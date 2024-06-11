""" sums the confusion rate of the files in talking_percents_combined.csv that are part+eval"""

import pandas as pd

df = pd.read_csv('talking_percents_combined.csv')
# filter the "filename" rows that have a 1 in "part+eval" column
df = df[df['part+eval'] == 1]

# open the DER reports
DER_1 = pd.read_csv('/home/aleph/diariziation_error_rate/evaluation_combined_db/DER_report.csv')
DER_2 = pd.read_csv('/home/aleph/diariziation_error_rate/evaluation_combined_db/DER_report_unbalanced.csv')

# iterate over every filename in the "filename" column
total_confusion_rate = 0
count = 0
for filename in df['filename']:
    # get the confusion rate of the file
    # preproceess filename
    filename = filename + ".txt"
    confusion_rate = DER_1[DER_1['filename'] == filename]['confusion2']
    total_confusion_rate +=float(confusion_rate.values[0])
    count += 1
    
print(total_confusion_rate/count)