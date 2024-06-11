import pandas as pd
import os
from talking_percents import talking_percents, over_threshold

# read talking_percents

df = pd.read_csv('talking_percents.csv')


# iterate over every filename in the "filename" column
for filename in df['filename']:
    # get the extension of the file
    filename_diarization = filename + '_diarization.csv'
    FOLDER = "/home/aleph/diariziation_error_rate/combined_database/hypothesis2"
    # search for the file in the folder
    for dirpath, dirnames, filenames in os.walk(FOLDER):
        # print(filenames)
        if filename_diarization in filenames:
            path_to_file = os.path.join(dirpath, filename_diarization)
            break
        else:
            path_to_file = None
    # check if the file was found

    if not path_to_file:
        #check in different folder as a txt
        filename_diarization = filename + '.txt'
        FOLDER = "/home/aleph/diariziation_error_rate/combined_database/hypothesis"
        # search for the file in the folder
        for dirpath, dirnames, filenames in os.walk(FOLDER):
            # print(filenames)
            if filename_diarization in filenames:
                path_to_file = os.path.join(dirpath, filename_diarization)
                break
            else:
                path_to_file = None
    
    # check if the file was found
    if not path_to_file:
        print(f"{filename_diarization} not found")
        continue

    # call talking_percent with the path to the file
    participantion_dict = talking_percents(path_to_file)
    # check if any participant spoke more than 70% of the time
    if over_threshold(participantion_dict):
        # add to the dataframe
        df.loc[df['filename'] == filename, 'over_threshold'] = True
    else:
        df.loc[df['filename'] == filename, 'over_threshold'] = False
    
# save the dataframe
df.to_csv('talking_percents_combined.csv', index=False)
