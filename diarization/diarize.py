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

pipeline = Pipeline.from_pretrained("config.yaml")
# check if GPU is available
if torch.cuda.is_available():
    pipeline.to(torch.device("cuda"))
else:
    pipeline.to(torch.device("cpu"))

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

def extract_audio(base_dir, audio_file, diarization_df, longest_speaker):
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
    if not os.path.exists(os.path.join(base_dir, 'diarization')):
        os.makedirs(os.path.join(base_dir, 'diarization'))
    output_file = os.path.join(base_dir, 'diarization', f'{audio_file.split("/")[-1][:-4]}_participant.wav')
    sf.write(output_file, new_waveform, sr)

def txt_to_diarization_df(manual_diarization_path):
    """
    This function takes the path to the manual diarization text file as input and returns
    a dataframe containing the manual diarization information."""
    diarization_df = pd.DataFrame()
    sr = 16000 # assumed sample rate

    with open(manual_diarization_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                start, end, speaker = line.split('\t')
                new_row = {'start': int(float(start) * sr), 
                           'end': int(float(end) * sr), 
                           'start [s]': round(float(start),3), 
                           'end [s]': round(float(end),3), 
                           'dur [s]' : round(float(end)-float(start),3), 
                           'speaker': speaker}
                diarization_df = pd.concat([diarization_df, pd.DataFrame(new_row, index=[0])], 
                                           ignore_index=True)
    return diarization_df

if __name__ == "__main__":

    cwd = os.getcwd()
    base_dir = os.path.join(cwd, 'vasco', "hypothesis")

    for root, dirs, files in os.walk(base_dir):
        for file in tqdm.tqdm(files):
            if file.lower().endswith('.wav'):
                try:
                    audio_file = os.path.join(root, file)
                    diarization, diarization_df, output_dict = diarize(audio_file)
                    longest_speaker = get_longest_speaker(diarization_df)
                    extract_audio(root, audio_file, diarization_df, longest_speaker)
                    # save diarization dataframe
                    diarization_df.to_csv(os.path.join(root, f'{file[:-4]}_diarization.csv'), index=False)
                except Exception as e:
                    print(f"Error with file {file}: {e}")
                    with open('error_log.txt', 'a') as f:
                        f.write(f"Error with file {file}: {e}\n")
                    continue
    # audios_path = os.path.join('/home/aleph/diariziation_error_rate/REDLAT/hypothesis/')

    # for root, dirs, files in os.walk(audios_path):
    #     for file in files:
    #         if file.endswith('.wav'):
    #             try:
    #                 manual_diarization_file = os.path.join(root, file).replace("hypothesis", "reference").replace('wav', 'txt')
    #                 manual_diarization_df = txt_to_diarization_df(manual_diarization_file)
    #                 audio_file = os.path.join(root, file)
    #                 diarization, diarization_df, output_dict = diarize(audio_file)
    #                 longest_speaker = "p"
    #                 extract_audio(root, audio_file, manual_diarization_df, longest_speaker)
    #             except Exception as e:
    #                 print(f"Error with file {file}: {e}")
    #                 continue