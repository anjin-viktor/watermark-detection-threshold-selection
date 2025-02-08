import sys
import math
import csv

detectW = 0
nonDetectW = 0
detectWFiltered = 0
nonDetectWFiltered = 0


def checkFixedThreshold(fileName, threshold):
    detected = 0

    with open(fileName) as csvfile:
        print(fileName)
        reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            correlation = float(row[0])


            if correlation >= threshold:
#                print(str(correlation))
                detected += 1

    return detected

if len(sys.argv) != 3:
    print("`filename` and optional `threshold` arguments expected")
    exit(1)

threshold = float(sys.argv[2])
results = checkFixedThreshold(sys.argv[1], threshold)
print("Watermarks detection count(statisctical threshold): " + str(results))

results = checkFixedThreshold(sys.argv[1], 33.651)
print("Watermarks detection count: " + str(results))
