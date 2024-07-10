# reads diarization csv's and converts them to audacity labels

import pandas as pd
import os

def csv2audacity_label(csv_file, label_file):
    df = pd.read_csv(csv_file)
    with open(label_file, 'w') as f:
        for i, row in df.iterrows():
            f.write(f"{row['start [s]']}\t{row['end [s]']}\t{row['speaker']}\n")

if __name__ == "__main__":
    base_dir = '/home/aleph/diariziation_error_rate/REDLAT/ASW/diarization'
    for file in os.listdir(base_dir):
        if file.endswith('.csv'):
            csv_file = os.path.join(base_dir, file)
            label_file = os.path.join(base_dir, f'{file[:-4]}.txt')
            csv2audacity_label(csv_file, label_file)