import math

from pathlib import Path
from scipy import optimize
from utils import detect_threshold
from watermarks import eblind_dlc
from watermarks import dct_watermark
from watermarks import dct_watermark_barni
from find_detect_thredhold_calc_correlations import calcThresholds

import csv


x_values = []
TP_values = []
FP_values = []
FN_values = []
FScore_values = []
FSScore_calc_num = 0
thresholds = []

def clearCache():
    global x_values, TP_values, FP_values, FN_values, FScore_values, FSScore_calc_num
    x_values = []
    TP_values = []
    FP_values = []
    FN_values = []
    FScore_values = []
    FSScore_calc_num = 0

def func(x):
    x_min = -1
    x_max = -1
    min_idx = -1
    max_idx = -1
    value = -1
    for idx, x_val in enumerate(x_values):
        if x_val <= x and x_val > x_min:
            x_min = x_val
            min_idx = idx
        if x_val >= x and (x_val < x_max or x_max == -1):
            x_max = x_val
            max_idx = idx

    if min_idx >= 0 and max_idx >= 0:
        if TP_values[min_idx] == TP_values[max_idx] and FP_values[min_idx] == FP_values[max_idx] and FN_values[min_idx] == FN_values[max_idx]:
            value = FScore_values[min_idx]
#            print("f_score(%f) = %f (found in map)" % (x, value))
            return 1 - value

    global thresholds
    result = detect_threshold.FScore(thresholds, float(x))
    x_values.append(x)
    FScore_values.append(result[0])
    TP_values.append(result[1])
    FP_values.append(result[3])
    FN_values.append(result[4])

    global FSScore_calc_num
    FSScore_calc_num = FSScore_calc_num + 1
    return 1 - result[0]

def readThresholds(watermark_name, ebmedding_level):
    global thresholds
    thresholds = detect_threshold.extractThresholds(detect_threshold.getThresholdsFilename(watermark_name, ebmedding_level))

watermark_names = ["dct_watermark_barni"]
watermarks = [dct_watermark_barni]
watermark_idx = 0

for watermark_name in watermark_names:
    csvfile = open("detect_threshold_by_embedding_" + watermark_name + ".csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

    for embedding_idx in range(0, len(watermarks[watermark_idx].levels)):
        calcThresholds(watermarks[watermark_idx], watermark_name, embedding_idx)

        clearCache()
        readThresholds(watermark_name, embedding_idx)
        min, max = detect_threshold.getSection(thresholds,0)
        minimizer = optimize.golden(func, brack=(0, max), full_output=True, tol=0.0000001)
        print(minimizer[0])
        writer.writerow([embedding_idx, minimizer[0]])

    watermark_idx = watermark_idx + 1
