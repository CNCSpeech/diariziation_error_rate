import os

results_folder = '/home/aleph/diariziation_error_rate/REDLAT/results'
for filename in os.listdir(results_folder):
    if filename.endswith('.csv'):
        #print the last line of the last column
        with open(os.path.join(results_folder, filename), 'r', encoding="utf-8") as f:
            lines = f.readlines()
            print(filename.replace("DER_report_", "").replace(".csv", ""),"confussion rate is: " ,
                   round(float(lines[-1].split(',')[-1].strip()), 2), "%")
