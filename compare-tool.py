import getopt, sys
import re
from statistics import mean

def parse_python(file):
    all_epochs = []
    all_changes = []
    for line in file:
        changes = []
        if line.startswith("Epoch:"):
            epoch_text = line.split(" ")
            epoch = list(filter(lambda x: x != '', epoch_text))
            all_epochs.append(epoch)
        elif line.startswith("["):
            line = line.strip()
            pre_changes = re.findall(r'(\(.+?\))',line)
            
            for pre_change in pre_changes:
                pre_change = pre_change.replace("(","")
                pre_change = pre_change.replace(")","")
                pre_change = pre_change.replace("\"","")
                pre_change = pre_change.replace("\'","")
                pre_change = pre_change.strip()
                change = pre_change.split(",")

                changes.append(change)
            all_changes.append(changes)
    return all_epochs, all_changes


def parse_p4(file):
    all_epochs = []
    all_changes = []
    all_flows = []

    for line in file:
        changes = []
        if line.startswith("Epoch:"):
            epoch_text = line.split(" ")
            epoch = list(filter(lambda x: x != '', epoch_text))
            all_epochs.append(epoch)
        elif line.startswith("Change:"):
            line = line[7:].strip()
            pre_changes = re.findall(r'(\(.+?\))',line)
            
            for pre_change in pre_changes:
                pre_change = pre_change.replace("(","")
                pre_change = pre_change.replace(")","")
                pre_change = pre_change.replace("\"","")
                pre_change = pre_change.replace("\'","")
                pre_change = pre_change.strip()
                change = pre_change.split(",")
                change = change[0:3]
                changes.append(change)
            all_changes.append(changes)
        elif line.startswith("Number of Flows:"):
            split_line = line.split(":")
            all_flows.append(int(split_line[1]))

    return all_epochs, all_changes, all_flows


def main():
    path = sys.argv[1]

    p4_file = open("python/" + path, 'r')
    python_file = open("p4/" + path, 'r')

    p4_thresholds, p4_changes = parse_python(p4_file)
    python_thresholds, python_changes = parse_python(python_file)

    threshold_errors = []
    threshold_percent_errors = []
    threshold_reldiff = []
    estimate_errors = []
    estimate_percent_errors = []

    true_positives = 0
    false_positives = 0
    less_detections = 0

    for i in range(len(p4_thresholds)):
        threshold_errors.append(float(python_thresholds[i][3]) - float(p4_thresholds[i][3]))
        threshold_reldiff.append((float(python_thresholds[i][3]) - float(p4_thresholds[i][3]))/float(python_thresholds[i][3]))
        threshold_percent_errors.append((float(p4_thresholds[i][3]) - float(python_thresholds[i][3])) / float(p4_thresholds[i][3]))

    for i in range(len(p4_changes)):
        less_detections = less_detections + (len(python_changes[i]) - len(p4_changes[i]))

        for change in p4_changes[i]:
            found = False
            for j in range(len(python_changes[i])):
                if change[0] == python_changes[i][j][0] and change[1] == python_changes[i][j][1]:
                    error = float(python_changes[i][j][2]) - float(change[2])
                    percent_error = (float(change[2]) - float(python_changes[i][j][2])) / float(change[2])
                    estimate_errors.append(error)
                    estimate_percent_errors.append(percent_error)
                    true_positives = true_positives + 1
                    found = True
                    break
            if found == False:
                false_positives = false_positives + 1

    for error in threshold_reldiff:
        print(error*100)

    #print("Threshold Percent Error:", mean(threshold_percent_errors)*100, "%")
    #print("Estimate Percent Error:", mean(estimate_percent_errors)*100, "%")
    #print("False Positives:",false_positives)
    #print("False Negatives:",less_detections+false_positives)
    #print("True Positives:", true_positives)
        
if __name__ == "__main__":
    main()