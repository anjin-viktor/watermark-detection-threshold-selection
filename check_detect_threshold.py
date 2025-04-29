import sys
import math
import csv

detectW = 0
nonDetectW = 0
detectWFiltered = 0
nonDetectWFiltered = 0
alpha = 0.003125 * 255

def checkFixedThreshold(fileName, threshold):
    detectW = 0
    nonDetectW = 0
    detectWFiltered = 0
    nonDetectWFiltered = 0

    detectFP = 0

    with open(fileName) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            rowThreshold = float(row[4])
            rowThresholdFiltered = float(row[5])
            rowNoWatermark = float(row[6])

            if rowThreshold >= threshold:
                detectW += 1
            else:
                nonDetectW += 1

            if rowThresholdFiltered >= threshold:
                detectWFiltered += 1
            else:
                nonDetectWFiltered += 1

            if rowNoWatermark >= threshold:
                detectFP += 1

    return [detectW, nonDetectW, detectWFiltered, nonDetectWFiltered, detectFP]

def checkStatisticalThreshold(fileName):
    detectW = 0
    nonDetectW = 0
    detectWFiltered = 0
    nonDetectWFiltered = 0

    detectFP = 0

    with open(fileName) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            rowThreshold = float(row[4]) / 255
            rowThresholdFiltered = float(row[5]) / 255
            rowNoWatermark = float(row[6]) / 255

            threshold = float(row[1])
            threshold *= alpha / 2
            if rowThreshold >= threshold:
                detectW += 1
            else:
                nonDetectW += 1

            threshold = float(row[2])
            threshold *= alpha / 2
            if rowThresholdFiltered >= threshold:
                detectWFiltered += 1
            else:
                nonDetectWFiltered += 1

            threshold = float(row[3])
            threshold *= alpha / 2
            if rowNoWatermark >= threshold:
                print(row[0])
                detectFP += 1

    return [detectW, nonDetectW, detectWFiltered, nonDetectWFiltered, detectFP]


if len(sys.argv) < 2:
    print("`path_to_csv` and optional `threshold` arguments expected")
    exit(1)

results = []
if len(sys.argv) == 3:
    threshold = float(sys.argv[2])
    results = checkFixedThreshold(sys.argv[1], threshold)
else:
    results = checkStatisticalThreshold(sys.argv[1])

print("Watermarks detected: " + str(results[0]))
print("Watermarks non-detected: " + str(results[1]))

print("Watermarks detected after filtering: " + str(results[2]))
print("Watermarks non-detected after filtering: " + str(results[3]))
print("Watermarks False Positive: " + str(results[4]))
