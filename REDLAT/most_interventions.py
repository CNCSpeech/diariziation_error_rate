import os


# get current working directory
cwd = os.getcwd()

# initialize a counter for the number of most intervantions, for both
count_p = 0
count_e = 0
count_CU = 0
count_MA = 0
count_LO = 0

for root, dirs, files in os.walk(os.path.join(cwd, "REDLAT", "reference")):
    for file in files:
        if file.endswith(".txt"):
            # open the file and read the contents
            # Initialize a dictionary to store total speaking time for each speaker
            speaking_times = {}
            with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
                data = f.read()
                for line in data.strip().split('\n'):
                    start, end, speaker = line.split()
                    start, end = float(start), float(end)
                    duration = end - start
                    if speaker in speaking_times:
                        speaking_times[speaker] += duration
                    else:
                        speaking_times[speaker] = duration
                # Find the speaker with the maximum speaking time
                max_speaker = max(speaking_times, key=speaking_times.get)
                max_time = speaking_times[max_speaker]
                
                if max_speaker.lower() == "p":
                    count_p += 1
                elif max_speaker.lower() == "e":
                    count_e += 1
                    if "CU" in file:
                        count_CU += 1
                    elif "MA" in file:
                        count_MA += 1
                    elif "LO" in file:
                        count_LO += 1
                    else:
                        print(file)
                else:
                    # print("Unknown speaker:", max_speaker, "in file", file)
                    # print(speaking_times)
                    # print(file)
                    continue
                # print(speaking_times)
            # break

# print("Number of most interventions by P:", count_p)
# print("Number of most interventions by E:", count_e)
# print("Number of most interventions by E in CU:", count_CU)
# print("Number of most interventions by E in MA:", count_MA)
# print("Number of most interventions by E in LO:", count_LO)

with open(os.path.join("REDLAT", "most_interventions_by_participant.txt"), "w", encoding="utf-8") as f:
    f.write("Number of most interventions by P: {}\n".format(count_p))
    f.write("Number of most interventions by E: {}\n".format(count_e))
    f.write("Number of most interventions by E in CU: {}\n".format(count_CU))
    f.write("Number of most interventions by E in MA: {}\n".format(count_MA))
    f.write("Number of most interventions by E in LO: {}\n".format(count_LO))
    f.write("Total number of files: {}\n".format(count_p + count_e))
    