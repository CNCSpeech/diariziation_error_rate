import os
import whisper
import pandas as pd

#load model
model = whisper.load_model("base", device="cuda")
# set model to transcribe in spanish
lang = "es"

bocanegra_path = "/home/aleph/diariziation_error_rate/datasets/bocanegra"
neutro_df = pd.read_csv(os.path.join(bocanegra_path, "NEUTRO_LIBRE.csv"))
motor_df = pd.read_csv(os.path.join(bocanegra_path, "MOTOR_LIBRE.csv"))

# add whisper transcription column
neutro_df["large-v2"] = ""
motor_df["larve-v2"] = ""
print(neutro_df.head())
print(motor_df.head())

for root, dirs, files in os.walk(bocanegra_path):
    # sort files in alphabetical order
    files.sort()
    for file in files:
        if file.endswith(".wav") and ("NEUTRO_LIBRE" in file or "MOTOR_LIBRE" in file):
            print(file.split(".")[0])
            transcription = model.transcribe(os.path.join(root, file), language=lang)
            print(transcription["text"])
            # save in corrsponding dataframe
            if "NEUTRO_LIBRE" in file:
                neutro_df.loc[neutro_df["FILENAME"] == file.split(".")[0], "large-v2"] = transcription["text"]
            elif "MOTOR_LIBRE" in file:
                motor_df.loc[motor_df["FILENAME"] == file.split(".")[0], "large-v2"] = transcription["text"]

        # save to csv
        neutro_df.to_csv(os.path.join(bocanegra_path, "NEUTRO_LIBRE.csv"), index=False)
        motor_df.to_csv(os.path.join(bocanegra_path, "MOTOR_LIBRE.csv"), index=False)

CETRAM_converted_path = "/home/aleph/diariziation_error_rate/datasets/CETRAM_converted"

for root, dirs, files in os.walk(CETRAM_converted_path):
    # sort files in alphabetical order
    files.sort()
    for file in files:
        if file.endswith(".wav"):
            print(file.split(".")[0])
            transcription = model.transcribe(os.path.join(root, file), language=lang)
            print(transcription["text"])
            # save in corrsponding dataframe
            if "NEUTRO_LIBRE" in file:
                neutro_df.loc[neutro_df["FILENAME"] == file.split(".")[0], "large-v2"] = transcription["text"]
            elif "MOTOR_LIBRE" in file:
                motor_df.loc[motor_df["FILENAME"] == file.split(".")[0], "large-v2"] = transcription["text"]

        # save to csv
        neutro_df.to_csv(os.path.join(bocanegra_path, "NEUTRO_LIBRE.csv"), index=False)
        motor_df.to_csv(os.path.join(bocanegra_path, "MOTOR_LIBRE.csv"), index=False)