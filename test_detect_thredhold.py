import os
import math

from concurrent.futures import ThreadPoolExecutor
from watermarks import dct_watermark_barni_lc
from watermarks import eblind_dlc
from watermarks import dct_watermark
from pathlib import Path
from tests import filter
from tests import transcode
import csv

filters_count = 6

def createReference(watermark, watermark_name, ebmedding_level, input_filename):
    os.makedirs("test_detect_thredhold", exist_ok=True)
    os.makedirs("test_detect_thredhold/" + watermark_name, exist_ok=True)

    name_preffix = "test_detect_thredhold/" + watermark_name + "/" + str(ebmedding_level)

    os.makedirs(name_preffix, exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = name_preffix + "/reference_" + str(filename_wo_ext) + ".bmp"
    output_name = name_preffix + "/watermarked_" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

    watermark.gen_reference(input_file, reference_name, ebmedding_level)
    watermark.embed(input_file, reference_name, output_name, ebmedding_level)

    filtered = name_preffix + "/filtered_" + str(filename_wo_ext) + ".bmp"
    transcode.run("webp", ["-quality", "25"], output_name, filtered)

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

    name_preffix = "test_detect_thredhold/" + watermark_name + "/" + str(ebmedding_level)
    reference_name = name_preffix + "/reference_" + str(filename_wo_ext) + ".bmp"
    output_name = name_preffix + "/watermarked_" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename
    filtered = name_preffix + "/filtered_" + str(filename_wo_ext) + ".bmp"

    result = watermark.get_correlation(output_name, reference_name, input_file)
    resultFiltered = watermark.get_correlation(filtered, reference_name, input_file)
    resultNoW = watermark.get_correlation(input_file, reference_name, input_file)

    result_dct_avg = watermark.get_avg_dct(output_name, reference_name, input_file)
    resultFiltered_dct_avg = watermark.get_avg_dct(filtered, reference_name, input_file)
    resultNoW_dct_avg = watermark.get_avg_dct(input_file, reference_name, input_file)
 
    return [input_filename, result_dct_avg, resultFiltered_dct_avg, resultNoW_dct_avg, result, resultFiltered, resultNoW]

def calcDetectionThresholdFileFalse(watermark, watermark_name, ebmedding_level, input_filename, test_filename):
    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')
 #   test_filename_wo_ext = Path(test_filename).with_suffix('')

    name_preffix = "test_detect_thredhold/" + watermark_name + "/" + str(ebmedding_level)
    reference_name = name_preffix + "/reference_" + str(filename_wo_ext) + ".bmp"
#    output_name = name_preffix + "/watermarked_" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

#    filtered = name_preffix + "/filtered_" + str(test_filename_wo_ext) + ".bmp"
#    result = watermark.get_correlation(filtered, reference_name, input_file)

    anoterWatermark_file = "images/" + test_filename
    resultAnoterWatermark = watermark.get_correlation(anoterWatermark_file, reference_name, input_file)

    return [resultAnoterWatermark]


def calcDetectionThreshold(watermark, watermark_name, ebmedding_level):
    threadPool = ThreadPoolExecutor()

    directory = os.fsencode("images/")
    os.makedirs("test_detect_thredhold_results", exist_ok=True)

    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(calcDetectionThresholdFile, watermark, watermark_name, ebmedding_level, filename)
        futures.append(future)

    csvfile = open("test_detect_thredhold_results/test_detect_threshold_" + watermark_name + "_" + str(ebmedding_level) + ".csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

    for future in futures:
        result = future.result()
        writer.writerow(result)

def calcDetectionThresholdFalse(watermark, watermark_name, ebmedding_level):
    os.makedirs("test_detect_thredhold_results", exist_ok=True)

    directory = os.fsencode("images/")

    for file in os.listdir(directory):
        threadPool = ThreadPoolExecutor()
        futures = []
        filename = os.fsdecode(file)
        for fileAnotherWT in os.listdir(directory):
            filenameAnotherWT = os.fsdecode(fileAnotherWT)
            if filename == filenameAnotherWT:
                continue

            future = threadPool.submit(calcDetectionThresholdFileFalse, watermark, watermark_name, ebmedding_level, filename, filenameAnotherWT)
            futures.append(future)

        csvfile = open("test_detect_thredhold_results/test_detect_threshold_false_" + watermark_name + "_" + str(ebmedding_level) + "_" + filename + ".csv", 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvfile)

        for future in futures:
            result = future.result()
            writer.writerow(result)


def calcThresholds(watermark, watermark_name, ebmedding_level):
    createReferences(watermark, watermark_name, ebmedding_level)
    calcDetectionThreshold(watermark, watermark_name, ebmedding_level)
#    calcDetectionThresholdFalse(watermark, watermark_name, ebmedding_level)

if __name__ == "__main__":
    watermark = dct_watermark_barni_lc
    watermark_name = "dct_watermark_barni_lc"


    ebmedding_levels = [10]
    for ebmedding_level in ebmedding_levels:
        print(ebmedding_level)
        calcThresholds(watermark, watermark_name, ebmedding_level)
