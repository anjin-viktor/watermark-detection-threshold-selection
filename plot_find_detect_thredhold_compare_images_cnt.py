import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import cm
import csv
from array import array
import math
from matplotlib.ticker import FuncFormatter


def calcMetrics(watermark_name, ebmedding_level):
    Cnt = []
    FScores = []
    X = []

    csvfile = "find_detect_threshold_" + watermark_name + "_" + str(ebmedding_level) + ".csv"

    with open(csvfile) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            Cnt.append(int(row[0]))
            X.append(float(row[1]))
            FScores.append(float(row[2]))

    FScoreLast = FScores[len(FScores) - 1]
    XLast = X[len(X) - 1]
    FScores.pop()
    X.pop()
    Cnt.pop()

#    avgCount = 1
#    FscoresAvg = []
#    for idx in range(0, len(FScores)):
#        avg = 0
#        avgCountCurr = avgCount
#        if len(FScores) - idx < avgCount:
#            avgCountCurr = len(FScores) - idx
#        for avgIdx in range(0, avgCountCurr):
#            avg += FScores[idx + avgIdx]
#        avg /= avgCountCurr
#        print(avg)
#        FscoresAvg.append(avg)

    diff = []
    diffX = []

    for fscore in FScores:
        cmp = math.fabs(fscore - FScoreLast)
        diff.append(cmp)

    for x in X:
        cmp = math.fabs(x - XLast)
        diffX.append(cmp)

    numImages = 350
    for i in range (0, len(FScores) - numImages):
        diff.pop()
        diffX.pop()
        Cnt.pop()

    diff = np.array(diff)
    diffX = np.array(diffX)
    return [diff, diffX, Cnt]

diffEBlindDLC_7, diffXEBlindDLC_7, cnt = calcMetrics("eblind_dlc", 7)
diffEBlindDLC_12, diffXEBlindDLC_12, cnt = calcMetrics("eblind_dlc", 12)
diffEBlindDLC_20, diffXEBlindDLC_20, cnt = calcMetrics("eblind_dlc", 20)
diffDCTWatermark_5, diffXDCTWatermark_5, cnt = calcMetrics("dct_watermark", 5)
diffDCTWatermark_10, diffXDCTWatermark_10, cnt = calcMetrics("dct_watermark", 10)
diffDCTWatermark_17, diffXDCTWatermark_17, cnt = calcMetrics("dct_watermark", 17)


fig, ax = plt.subplots(1, 1)


Cnt = np.array(cnt)
diffEBlindDLC_7 = np.array(diffEBlindDLC_7)
diffEBlindDLC_12 = np.array(diffEBlindDLC_12)
diffEBlindDLC_20 = np.array(diffEBlindDLC_20)
diffDCTWatermark_5 = np.array(diffDCTWatermark_5)
diffDCTWatermark_10 = np.array(diffDCTWatermark_10)
diffDCTWatermark_17 = np.array(diffDCTWatermark_17)

diffXEBlindDLC_7 = np.array(diffXEBlindDLC_7)
diffXEBlindDLC_12 = np.array(diffXEBlindDLC_12)
diffXEBlindDLC_20 = np.array(diffXEBlindDLC_20)
diffXDCTWatermark_5 = np.array(diffXDCTWatermark_5)
diffXDCTWatermark_10 = np.array(diffXDCTWatermark_10)
diffXDCTWatermark_17 = np.array(diffXDCTWatermark_17)

ax.set_xlabel('Количество изображений')


##delta F-score
ax.plot(Cnt, diffEBlindDLC_7)
ax.plot(Cnt, diffEBlindDLC_12)
ax.plot(Cnt, diffEBlindDLC_20)
ax.plot(Cnt, diffDCTWatermark_5)
ax.plot(Cnt, diffDCTWatermark_10)
ax.plot(Cnt, diffDCTWatermark_17)


ax.set_ylabel('|F-opt(8091) - F-opt(n)|')
ax.set_title("Отклонение оптимального значения F-меры")
ax.legend(["E_BLIND/D_CC, \u03B1=0,059", "E_BLIND/D_CC, \u03B1=0,1", "E_BLIND/D_CC, \u03B1=0,19", "DCT-ЦВЗ, \u03B1=0,039", "DCT-ЦВЗ, \u03B1=0,086", "DCT-ЦВЗ, \u03B1=0,156"])

#
##delta X-opt
#ax.plot(Cnt, diffXEBlindDLC_7)
#ax.plot(Cnt, diffXEBlindDLC_12)
#ax.plot(Cnt, diffXEBlindDLC_20)
#ax.plot(Cnt, diffXDCTWatermark_5)
#ax.plot(Cnt, diffXDCTWatermark_10)
#ax.plot(Cnt, diffXDCTWatermark_17)

#ax.set_ylabel('|\u03F4-opt(8091) - \u03F4-opt(n)|')
#ax.set_title("Отклонение оптимального порогового значения обнаружения")
#ax.legend(["E_BLIND/D_CC, \u03B1=0,059", "E_BLIND/D_CC, \u03B1=0,1", "E_BLIND/D_CC, \u03B1=0,19", "DCT-ЦВЗ, \u03B1=0,039", "DCT-ЦВЗ, \u03B1=0,086", "DCT-ЦВЗ, \u03B1=0,156"])

def comma_formatter(x, pos):
    x_float = float(x)
    x_float = round(x_float, 3)
    x = str(x_float)
    return str(x).replace('.', ',')
 
#plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))
plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))


plt.show()
