# recives a diarization.csv file and prints out the percentage of time each speaker spoke
# important

import pandas as pd

def talking_percents_csv(diarization_csv):
    """
    This function reads a diarization csv file and prints out the percentage of time each speaker spoke"""
    # read the csv file
    df = pd.read_csv(diarization_csv)

    # get the total time as the sum of the durations of each segment which is the dur[s] column
    total_time = df['end [s]'].sum() - df['start [s]'].sum()

    # get the time each speaker spoke
    participantion_dict = {"total_time": total_time}
    speakers = df['speaker'].unique()
    for speaker in speakers:
        speaker_time = df[df['speaker'] == speaker]['end [s]'].sum() - df[df['speaker'] == speaker]['start [s]'].sum()
        participantion_dict[speaker] = speaker_time

    return participantion_dict

def talking_percents_txt(diarization_txt):
    """
    This function reads a diarization txt file and prints out the percentage of time each speaker spoke"""

    # read the txt file
    with open(diarization_txt, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        # start, end and speaker are in the same line, divided by a tab
        # the first line is the total time
        total_time = 0
        for line in lines:
            total_time += float(line.split('\t')[1]) - float(line.split('\t')[0])

        # get the time each speaker spoke
        participantion_dict = {"total_time": total_time}
        for line in lines[1:]:
            speaker = line.split('\t')[2]
            speaker_time = float(line.split('\t')[1]) - float(line.split('\t')[0])
            if speaker in participantion_dict:
                participantion_dict[speaker] += speaker_time
            else:
                participantion_dict[speaker] = speaker_time

    return participantion_dict


def talking_percents(diarization):
    if diarization.endswith('.csv'):
        return talking_percents_csv(diarization)
    elif diarization.endswith('.txt'):
        return talking_percents_txt(diarization)


def over_threshold(participantion_dict, threshold=.7):
    """
    This function receives the output of talking_percents and 
    a threshold and returns TRUE if a participant spoke more than the threshold
    and FALSE otherwise. 
    theshold is a number between 0 and 1, interpreted as a percentage"""
    
    for speaker in participantion_dict.keys():
        if speaker != 'total_time':
            if participantion_dict[speaker] > threshold * participantion_dict['total_time']:
                return True
    return False

#test
if __name__ == '__main__':
    txt_file = "/home/aleph/diariziation_error_rate/combined_database/hypothesis/AS/CETRAM_AMG-0012_LecturaDeParrafo.txt"
    participation = talking_percents_txt(txt_file)
    print(participation)
    print(over_threshold(participation, .7))
