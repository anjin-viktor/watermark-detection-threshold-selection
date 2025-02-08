import os
import math

from concurrent.futures import ThreadPoolExecutor
from watermarks import eblind_dlc
from watermarks import dct_watermark
from watermarks import e_perc_shape
from pathlib import Path
from tests import filter
from tests import transcode
from scipy import optimize
import csv



import math

from pathlib import Path
from scipy import optimize
from utils import detect_threshold


x_values = []
TP_values = []
FP_values = []
FN_values = []
FScore_values = []
FSScore_calc_num = 0
thresholds = []

TP = []
TN = []
FP = []
FN = []


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
    thresholds = detect_threshold.extractThresholds(detect_threshold.getThresholdsFilename(watermark_name, ebmedding_level))
    return thresholds

def testWatermark(watermark_name, ebmedding_level):

    thresholds_full = readThresholds(watermark_name, ebmedding_level)
    files_cnt = []
    for i in range(5, len(thresholds_full), 1):
        files_cnt.append(i)

    csvfile = open("find_detect_threshold_" + watermark_name + "_" + str(ebmedding_level) + ".csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

    for cnt in files_cnt:
        global thresholds
        thresholds = []
        for i in range(0, cnt):
            thresholds.append(thresholds_full[i])

        min, max = detect_threshold.getSection(thresholds,0)
        minimizer = optimize.golden(func, brack=(0, max), full_output=True, tol=0.0000001)
        result = detect_threshold.FScore(thresholds_full, float(minimizer[0]))

#        print ("%d: x=%f, FScore=%f, number of calculations=%d, TP=%d, FP=%d, FN=%d" % (cnt, minimizer[0], 1-minimizer[1], FSScore_calc_num, result[1], result[3], result[4]))
        writer.writerow([str(cnt), str(minimizer[0]), str(result[0]), str(FSScore_calc_num)])
        clearCache()

    thresholds = thresholds_full
    min, max = detect_threshold.getSection(thresholds,0)
    minimizer = optimize.golden(func, brack=(0, max), full_output=True, tol=0.0000001)
    result = detect_threshold.FScore(thresholds, float(minimizer[0]))

#    print ("%d: x=%f, FScore=%f, number of calculations=%d, TP=%d, FP=%d, FN=%d" % (len(thresholds_full), minimizer[0], 1-minimizer[1], FSScore_calc_num, result[1], result[3], result[4]))
    writer.writerow([len(thresholds_full), str(minimizer[0]), str(1-minimizer[1]), str(FSScore_calc_num)])
    clearCache()

ebmedding_levels = [7, 12, 20, 5, 10, 17]
watermark_names = ["eblind_dlc", "eblind_dlc", "eblind_dlc", "dct_watermark", "dct_watermark", "dct_watermark"]

#ebmedding_levels = [7]
#watermark_names = ["eblind_dlc"]


for idx in range(0, len(ebmedding_levels)):
    testWatermark(watermark_names[idx], ebmedding_levels[idx])
