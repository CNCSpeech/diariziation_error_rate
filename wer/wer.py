import os
from jiwer import wer
import pandas as pd

wer_dir = "/home/aleph/diariziation_error_rate/wer"
neutro_df = pd.read_csv(os.path.join(wer_dir, "NEUTRO_LIBRE_transcription.csv"))
motor_df = pd.read_csv(os.path.join(wer_dir, "MOTOR_LIBRE_transcription.csv"))

# calculate over all the dataset
wer_neutro = []
wer_motor = []
for index, row in neutro_df.iterrows():
    try:
        reference = row["TRANSCRIPT"]
        hypothesis = row["large-v2"]
        reference = reference.lower()
        hypothesis = hypothesis.lower()
        reference = reference.replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("?", "").replace("¿", "").replace("¡", "")
        hypothesis = hypothesis.replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("?", "")
        error = wer(reference, hypothesis)
        wer_neutro.append(error)
    except AttributeError:
        print("ERROR: ", reference, hypothesis)
for index, row in motor_df.iterrows():
    try:
        reference = row["TRANSCRIPT"]
        hypothesis = row["large-v2"]
        reference = reference.lower()
        hypothesis = hypothesis.lower()
        reference = reference.replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("?", "").replace("¿", "").replace("¡", "")
        hypothesis = hypothesis.replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("?", "")
        error = wer(reference, hypothesis)
        wer_motor.append(error)
    except AttributeError:
        print("ERROR: ", reference, hypothesis)
print("WER NEUTRO: ", sum(wer_neutro)/len(wer_neutro))
print("WER MOTOR: ", sum(wer_motor)/len(wer_motor))

average_wer = (sum(wer_neutro)/len(wer_neutro) + sum(wer_motor)/len(wer_motor))/2

print("AVERAGE WER: ", average_wer)