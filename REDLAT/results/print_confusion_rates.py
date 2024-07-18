import os

RESULTS_FOLDER = '/home/aleph/diariziation_error_rate/REDLAT/results'

total_path = '/home/aleph/diariziation_error_rate/REDLAT/results/DER_report.csv'

# print the total DER
with open(total_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    print("\nTotal Confusion rate is: ", round(float(lines[-1].split(',')[-1].strip()), 2), "%")

for folder in os.listdir(RESULTS_FOLDER):
    if os.path.isdir(os.path.join(RESULTS_FOLDER, folder)):
        print("\n")
        print(folder)
        for filename in os.listdir(os.path.join(RESULTS_FOLDER, folder)):
            if filename.endswith('.csv'):
                #print the last line of the last column
                with open(os.path.join(RESULTS_FOLDER, folder, filename), 'r', encoding="utf-8") as f:
                    lines = f.readlines()
                    print(filename.replace("DER_report_", "").replace(".csv", ""),"confussion rate is: " ,
                           round(float(lines[-1].split(',')[-1].strip()), 2), "%")
        
