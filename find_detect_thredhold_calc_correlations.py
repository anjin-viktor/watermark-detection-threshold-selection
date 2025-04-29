import os
import math

from concurrent.futures import ThreadPoolExecutor
from watermarks import eblind_dlc
from watermarks import dct_watermark
from watermarks import e_perc_shape
from watermarks import dct_watermark_barni_lc
from pathlib import Path
from tests import filter
from tests import transcode
import csv

filters_count = 6

def createReference(watermark, watermark_name, ebmedding_level, input_filename):
    os.makedirs("detect_fixed_strength", exist_ok=True)
    os.makedirs("detect_fixed_strength/" + watermark_name, exist_ok=True)

    name_preffix = "detect_fixed_strength/" + watermark_name + "/" + str(ebmedding_level)

    os.makedirs(name_preffix, exist_ok=True)
    os.makedirs(name_preffix + "/reference/", exist_ok=True)
    os.makedirs(name_preffix + "/filter_dctdnoiz_5/", exist_ok=True)
    os.makedirs(name_preffix + "/filter_dctdnoiz_10/", exist_ok=True)
    os.makedirs(name_preffix + "/unsharp_blur/", exist_ok=True)
    os.makedirs(name_preffix + "/unsharp_sharp/", exist_ok=True)
    os.makedirs(name_preffix + "/transcode_1/", exist_ok=True)
    os.makedirs(name_preffix + "/transcode_25/", exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = name_preffix + "/reference/reference_" + str(filename_wo_ext) + ".bmp"
    output_name = name_preffix + "/reference/watermarked_" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

    watermark.gen_reference(input_file, reference_name, ebmedding_level)
    watermark.embed(input_file, reference_name, output_name, ebmedding_level)

    dctdnoiz_5_name_watermark = name_preffix + "/filter_dctdnoiz_5/" + str(filename_wo_ext) + "with_watermark.bmp"
    filter.run("dctdnoiz=s=5", output_name, dctdnoiz_5_name_watermark)

    dctdnoiz_10_name_watermark = name_preffix + "/filter_dctdnoiz_10/" + str(filename_wo_ext) + "with_watermark.bmp"
    filter.run("dctdnoiz=s=10", output_name, dctdnoiz_10_name_watermark)

    unsharp_name_watermark = name_preffix + "/unsharp_blur/" + str(filename_wo_ext) + "with_watermark.bmp"
    filter.run("unsharp=3:3:-0.25:3:3:-0.25", output_name, unsharp_name_watermark)

    sharp_name_watermark = name_preffix + "/unsharp_sharp/" + str(filename_wo_ext) + "with_watermark.bmp"
    filter.run("unsharp=3:3:0.25:3:3:0.25", output_name, sharp_name_watermark)

    transcode_1_name_watermark = name_preffix + "/transcode_1/" + str(filename_wo_ext) + "with_watermark.bmp"
    transcode.run("mjpeg", ["-qmin", "1", "-qmax", "1"], output_name, transcode_1_name_watermark)

    transcode_25_name_watermark = name_preffix + "/transcode_25/" + str(filename_wo_ext) + "with_watermark.bmp"
    transcode.run("mjpeg", ["-qmin", "25", "-qmax", "25"], output_name, transcode_25_name_watermark)

    dctdnoiz_5_name_wo_watermark = name_preffix + "/filter_dctdnoiz_5/" + str(filename_wo_ext) + "wo_watermark.bmp"
    filter.run("dctdnoiz=s=5", input_file, dctdnoiz_5_name_wo_watermark)

    dctdnoiz_10_name_wo_watermark = name_preffix + "/filter_dctdnoiz_10/" + str(filename_wo_ext) + "wo_watermark.bmp"
    filter.run("dctdnoiz=s=10", input_file, dctdnoiz_10_name_wo_watermark)

    unsharp_name_wo_watermark = name_preffix + "/unsharp_blur/" + str(filename_wo_ext) + "wo_watermark.bmp"
    filter.run("unsharp=3:3:-0.25:3:3:-0.25", input_file, unsharp_name_wo_watermark)

    sharp_name_wo_watermark = name_preffix + "/unsharp_sharp/" + str(filename_wo_ext) + "wo_watermark.bmp"
    filter.run("unsharp=3:3:0.25:3:3:0.25", input_file, sharp_name_wo_watermark)

    transcode_1_name_wo_watermark = name_preffix + "/transcode_1/" + str(filename_wo_ext) + "wo_watermark.bmp"
    transcode.run("mjpeg", ["-qmin", "1", "-qmax", "1"], input_file, transcode_1_name_wo_watermark)

    transcode_25_name_wo_watermark = name_preffix + "/transcode_25/" + str(filename_wo_ext) + "wo_watermark.bmp"
    transcode.run("mjpeg", ["-qmin", "25", "-qmax", "25"], input_file, transcode_25_name_wo_watermark)



def createReferences(watermark, watermark_name, ebmedding_level):
    threadPool = ThreadPoolExecutor()

    directory = os.fsencode("images/")

    futures = [];
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(createReference, watermark, watermark_name, ebmedding_level, filename)
        futures.append(future)

    for future in futures:
        future.result()

def calcDetectionThresholdFile(watermark, watermark_name, ebmedding_level, input_filename):
    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    name_preffix = "detect_fixed_strength/" + watermark_name + "/" + str(ebmedding_level)

    reference_name = name_preffix + "/reference/reference_" + str(filename_wo_ext) + ".bmp"
    watermarked_name = name_preffix + "/reference/watermarked_" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename
    dctdnoiz_5_name_watermark = name_preffix + "/filter_dctdnoiz_5/" + str(filename_wo_ext) + "with_watermark.bmp"
    dctdnoiz_10_name_watermark = name_preffix + "/filter_dctdnoiz_10/" + str(filename_wo_ext) + "with_watermark.bmp"
    unsharp_name_watermark = name_preffix + "/unsharp_blur/" + str(filename_wo_ext) + "with_watermark.bmp"
    sharp_name_watermark = name_preffix + "/unsharp_sharp/" + str(filename_wo_ext) + "with_watermark.bmp"
    transcode_1_name_watermark = name_preffix + "/transcode_1/" + str(filename_wo_ext) + "with_watermark.bmp"
    transcode_25_name_watermark = name_preffix + "/transcode_25/" + str(filename_wo_ext) + "with_watermark.bmp"
    dctdnoiz_5_name_wo_watermark = name_preffix + "/filter_dctdnoiz_5/" + str(filename_wo_ext) + "wo_watermark.bmp"
    dctdnoiz_10_name_wo_watermark = name_preffix + "/filter_dctdnoiz_10/" + str(filename_wo_ext) + "wo_watermark.bmp"
    unsharp_name_wo_watermark = name_preffix + "/unsharp_blur/" + str(filename_wo_ext) + "wo_watermark.bmp"
    sharp_name_wo_watermark = name_preffix + "/unsharp_sharp/" + str(filename_wo_ext) + "wo_watermark.bmp"
    transcode_1_name_wo_watermark = name_preffix + "/transcode_1/" + str(filename_wo_ext) + "wo_watermark.bmp"
    transcode_25_name_wo_watermark = name_preffix + "/transcode_25/" + str(filename_wo_ext) + "wo_watermark.bmp"

    result = watermark.get_correlation(watermarked_name, reference_name, input_file)
    resultDct5 = watermark.get_correlation(dctdnoiz_5_name_watermark, reference_name, input_file)
    resultDct10 = watermark.get_correlation(dctdnoiz_10_name_watermark, reference_name, input_file)
    resultUnsharp = watermark.get_correlation(unsharp_name_watermark, reference_name, input_file)
    resultSharp = watermark.get_correlation(sharp_name_watermark, reference_name, input_file)
    resultJpeg1 = watermark.get_correlation(transcode_1_name_watermark, reference_name, input_file)
    resultJpeg25 = watermark.get_correlation(transcode_25_name_watermark, reference_name, input_file)

    resultNoW = watermark.get_correlation(input_file, reference_name, input_file)
    resultNoWDct5 = watermark.get_correlation(dctdnoiz_5_name_wo_watermark, reference_name, input_file)
    resultNoWDct10 = watermark.get_correlation(dctdnoiz_10_name_wo_watermark, reference_name, input_file)
    resultNoWUnsharp = watermark.get_correlation(unsharp_name_wo_watermark, reference_name, input_file)
    resultNoWSharp = watermark.get_correlation(sharp_name_wo_watermark, reference_name, input_file)
    resultNoWJpeg1 = watermark.get_correlation(transcode_1_name_wo_watermark, reference_name, input_file)
    resultNoWJpeg25 = watermark.get_correlation(transcode_25_name_wo_watermark, reference_name, input_file)
 
    return [result, resultDct5, resultDct10, resultUnsharp, resultSharp, resultJpeg1, resultJpeg25, resultNoW, resultNoWDct5, resultNoWDct10, resultNoWUnsharp, resultNoWSharp, resultNoWJpeg1, resultNoWJpeg25]


def calcDetectionThreshold(watermark, watermark_name, ebmedding_level):
    threadPool = ThreadPoolExecutor()

    directory = os.fsencode("images/")

    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(calcDetectionThresholdFile, watermark, watermark_name, ebmedding_level, filename)
        futures.append(future)

    csvfile = open("detect_thresholds_" + watermark_name + "_" + str(ebmedding_level) + ".csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

    for future in futures:
        result = future.result()
        writer.writerow(result)

def calcThresholds(watermark, watermark_name, ebmedding_level):
    createReferences(watermark, watermark_name, ebmedding_level)
    calcDetectionThreshold(watermark, watermark_name, ebmedding_level)

if __name__ == "__main__":
    ebmedding_level = 10
    calcThresholds(dct_watermark_barni_lc, "dct_watermark_barni_lc", ebmedding_level)


    ebmedding_level = 7
    watermark = eblind_dlc
    watermark_name = "eblind_dlc"
    calcThresholds(watermark, watermark_name, ebmedding_level)
    ebmedding_level = 12
    calcThresholds(watermark, watermark_name, ebmedding_level)
    ebmedding_level = 20
    calcThresholds(watermark, watermark_name, ebmedding_level)


    ebmedding_level = 5
    watermark = dct_watermark
    watermark_name = "dct_watermark"
    calcThresholds(watermark, watermark_name, ebmedding_level)
    ebmedding_level = 10
    calcThresholds(watermark, watermark_name, ebmedding_level)
    ebmedding_level = 17
    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 1
#    watermark = e_perc_shape
#    watermark_name = "e_perc_shape"
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 2
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 3
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 5
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 29
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 10
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 15
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 20
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 23
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 25
#    calcThresholds(watermark, watermark_name, ebmedding_level)

#    ebmedding_level = 27
#    calcThresholds(watermark, watermark_name, ebmedding_level)
