import csv

filters_count = 6


def FScore(images_thresholds, threshold):

    resultsTP = 0
    resultsFP = 0
    resultsFN = 0
    resultsTN = 0

    for row in images_thresholds:
        resultTP = row[0] > threshold
        for i in range(1, filters_count+1):
            resultTP += row[i] > threshold

        resultFN = filters_count + 1 - resultTP

        resultFP = row[filters_count + 1] > threshold
        for i in range(1, filters_count+1):
            resultFP += row[filters_count + 1 + i] > threshold

        resultTN = filters_count + 1 - resultFP

        resultsTP += resultTP
        resultsFP += resultFP
        resultsFN += resultFN
        resultsTN += resultTN

    FScore = 2 * resultsTP / (2 * resultsTP + resultsFP + resultsFN)

    return [FScore, resultsTP, resultsTN, resultsFP, resultsFN]


def calcFScoreGraph(image_thresholds, file_dst, min=-1, max=-1):
    csvfile = open(file_dst, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

    itemsCount = 100 

    idx = 0
    FScores = [0] * itemsCount
    TP = [0] * itemsCount
    TN = [0] * itemsCount
    FP = [0] * itemsCount
    FN = [0] * itemsCount
    if min == -1 or max == -1:
        min, max = getSection(image_thresholds, 0)

    threshold_values = []
    step = (max - min) / (itemsCount - 1)
    for i in range(0, itemsCount):
        threshold_values.append(min + i * step)

    for threshold in threshold_values:
        res = FScore(image_thresholds, threshold)
        FScores[idx] = res[0]
        cnt = res[1] + res[2] + res[3] + res[4]
        TP[idx] = res[1] / cnt
        TN[idx] = res[2] / cnt
        FP[idx] = res[3] / cnt
        FN[idx] = res[4] / cnt

        idx = idx + 1

    writer.writerow(threshold_values)
    writer.writerow(FScores)
    writer.writerow(TP)
    writer.writerow(TN)
    writer.writerow(FP)
    writer.writerow(FN)

def getThresholdsFilename(watermark_name, ebmedding_level):
    return "detect_thresholds_" + watermark_name + "_" + str(ebmedding_level) + ".csv"

def getScoresFilename(watermark_name, ebmedding_level):
    return watermark_name + "_detect_fixed_strength_" + str(ebmedding_level) + ".csv"

def extractThresholds(filename):
    csvfileInput = open(filename, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csvfileInput, quoting=csv.QUOTE_NONNUMERIC)
    thresholds = []
    for row in reader:
        thresholds.append(row)
    return thresholds

def getSection(thresholds, remove_percentage=25):
    min = -100
    max = -100

    threshold_values = []

    for row in thresholds:
        for row_value in row:
            threshold_values.append(row_value)
            if row_value < min or min == -100:
                min = row_value

            if row_value > max or max == -100:
                max = row_value

    threshold_values.sort()

    remove_cnt = (int)(len(threshold_values) * remove_percentage / 100)

    for i in range(0, remove_cnt):
        threshold_values.pop()

    return [threshold_values[0], threshold_values[len(threshold_values) - 1]]

if __name__ == "__main__":

    watermark_name = "eblind_dlc"
    ebmedding_level = 7
#    calcThresholds(getThresholdsFilename(watermark_name, ebmedding_level), getScoresFilename(watermark_name, ebmedding_level))
    thresholds = extractThresholds(getThresholdsFilename(watermark_name, ebmedding_level))
    print(FScore(thresholds, 0.0005))
    print(FScore(thresholds, 0.000250))
    print(FScore(thresholds, 0.007))
    print(FScore(thresholds, 0.017922))
    print(getSection(thresholds))
#    calcFScoreGraph(thresholds, getScoresFilename(watermark_name, ebmedding_level))
