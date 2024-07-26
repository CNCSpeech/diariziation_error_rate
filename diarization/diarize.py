"""
This scripts takes care of diarization of the audio files, via the pyannote-audio library.
First, we extract the segmented speakers in the form of a text file. Then, we determine the 
speaker with the highest speaking time in seconds. We then extract the audio of the speaker 
and save it in a separate file."""

import os
import pandas as pd
import tqdm
from pyannote.audio import Pipeline
import torch
import torchaudio
import soundfile as sf
import numpy as np

from passwords import AUTH_TOKEN
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                    use_auth_token=AUTH_TOKEN)
# check if GPU is available
if torch.cuda.is_available():
    pipeline.to(torch.device("cuda"))
else:
    pipeline.to(torch.device("cpu"))

# audios (.wav) should be placed in the followin folder (modify if necessary)
base_dir = os.path.join(os.getcwd(), 'combined_database','reference', 'FA')

def diarize(audio_file):
    """
    This function takes an audio file as input and returns the diarization object,
    diarization dataframe and a dictionary containing the number of speakers and 
    their speaking time."""
    waveform, sr = torchaudio.load(audio_file) # Audio must be a torch tensor
    diarization = pipeline({'waveform':waveform,'sample_rate':sr}, min_speakers=1, max_speakers=2)
    diarization_df = pd.DataFrame()

    # Count number of speakers
    speakers = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if speaker not in speakers:
            speakers.append(speaker)

        dur = turn.end-turn.start
        new_row = {'start': int(turn.start * sr), 
                   'end': int(turn.end * sr), 
                   'start [s]': round(turn.start,3), 
                   'end [s]': round(turn.end,3), 
                   'dur [s]' : round(dur,3), 
                   'speaker': speaker}
        diarization_df = pd.concat([diarization_df, pd.DataFrame(new_row, index=[0])], 
                                   ignore_index=True)

    num_speakers = len(speakers)
    speaker_durs = diarization_df.groupby(['speaker'], as_index=False).sum()

    output_dict = dict()
    output_dict['filename'] = audio_file
    output_dict['num_speakers'] = num_speakers

    for _, row in speaker_durs.iterrows():
        output_dict[str(row['speaker'])] = row['dur [s]']

    return diarization, diarization_df, output_dict

def get_longest_speaker(diarization_df):
    """
    This function takes the diarization dataframe as input and returns the speaker
    with the highest speaking time in seconds."""
    speaker_durs = diarization_df.groupby(['speaker'], as_index=False).sum()
    speaker_durs = speaker_durs.sort_values(by='dur [s]', ascending=False)
    longest_speaker = speaker_durs.iloc[0]['speaker']
    return longest_speaker

def extract_audio(audio_file, diarization_df, longest_speaker):
    """
    This function takes the audio file, diarization dataframe and the speaker with the
    highest speaking time as input and deletes any intervention from other speakers.
    Resulting audio should be of equal lenght to the original audio."""
    waveform, sr = sf.read(audio_file)
    new_waveform = np.zeros_like(waveform)
    for _, row in diarization_df.iterrows():
        if row['speaker'] != longest_speaker:
            new_waveform[row['start']:row['end']] = 0   # Delete audio from other speakers
        else:
            new_waveform[row['start']:row['end']] = waveform[row['start']:row['end']]
    output_file = os.path.join(base_dir, 'diarization', f'{audio_file.split("/")[-1][:-4]}_participant.wav')
    sf.write(output_file, new_waveform, sr)

if __name__ == "__main__":
    humans = ['FA', 'JP', 'LG', 'MA', 'MC', 'NP', 'SG']

    for human in humans:
        print(f"Processing {human}")
        base_dir = os.path.join(os.getcwd(), 'combined_database','reference', human)


        output_dir = base_dir.replace('reference', 'hypothesis')
        os.makedirs(output_dir, exist_ok=True)
        for file in tqdm.tqdm(os.listdir(base_dir)):
            if file.endswith('.wav'):
                try:
                    audio_file = os.path.join(base_dir, file)
                    # check if file has already been processed
                    if os.path.exists(os.path.join(output_dir, f'{file[:-4]}_diarization.csv')):
                        continue
                    diarization, diarization_df, output_dict = diarize(audio_file)
                    # longest_speaker = get_longest_speaker(diarization_df)
                    # extract_audio(audio_file, diarization_df, longest_speaker)
                    diarization_df.to_csv(os.path.join(output_dir, f'{file[:-4]}_diarization.csv'), index=False)
                except Exception as e:
                    with open(os.path.join(output_dir, 'error_log.txt'), 'a', encoding="utf-8") as f:
                        f.write(f"Error with {file}: {e}\n")
                    continue
