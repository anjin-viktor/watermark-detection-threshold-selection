import os
import csv

from concurrent.futures import ThreadPoolExecutor
from watermarks import eblind_dlc
from watermarks import dct_watermark
from watermarks import e_perc_shape
from utils import psnr
from utils import wmaf
from pathlib import Path
from tests import filter
from tests import transcode

levels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

def createReference(watermark, input_filename, level):
    os.makedirs("detect", exist_ok=True)
    os.makedirs("detect/" + str(level), exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = "detect/" + str(level) + "/reference_" + str(filename_wo_ext) + ".bmp"
    output_name = "detect/" + str(level) + "/watermarked_" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

    watermark.gen_reference(input_file, reference_name, level)
    watermark.embed(input_file, reference_name, output_name)


def createReferences(watermark):
    threadPool = ThreadPoolExecutor()

    for level in levels:
        directory = os.fsencode("images/")

        futures = [];
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            future = threadPool.submit(createReference, watermark, filename, level)
            futures.append(future)

        for future in futures:
            future.result()

def calcDetectionThreshold(watermark, input_filename, detect_level):
    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    results = []
    for level in levels:
        reference_name = "detect/" + str(level) + "/reference_" + str(filename_wo_ext) + ".bmp"
        watermarked_name = "detect/" + str(level) + "/watermarked_" + str(filename_wo_ext) + ".bmp"
        input_file = "images/" + input_filename
        result = watermark.detect(watermarked_name, reference_name, input_file, detect_level)
        results.append(result)

    return results

def calcDetectionFalsePositive(watermark, input_filename, detect_level):
    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    results = []
    for level in levels:
        reference_name = "detect/" + str(level) + "/reference_" + str(filename_wo_ext) + ".bmp"
        input_file = "images/" + input_filename
        result = watermark.detect(input_file, reference_name, input_file, detect_level)
        results.append(result)

    return results

def calcDetectionThresholds(watermark, watermark_name):
    threadPool = ThreadPoolExecutor()

    csvfile = open(watermark_name + "_detect.csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)


    for detect_level in levels:
        directory = os.fsencode("images/")

        print("level: " + str(detect_level))

        futures = []
        cnt = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            future = threadPool.submit(calcDetectionThreshold, watermark, filename, detect_level)
            futures.append(future)
            cnt = cnt + 1

        resultsTP = []
        for future in futures:
            result = future.result()

            if len(resultsTP) != len(result):
                resultsTP = [0] * len(result)

            for i, val in enumerate(result):
                resultsTP[i] += int(val)

        resultsFN = [0] * len(resultsTP)
        for i, val in enumerate(resultsTP):
            resultsFN[i] = cnt - resultsTP[i]

        futures = []
        cnt = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            future = threadPool.submit(calcDetectionFalsePositive, watermark, filename, detect_level)
            futures.append(future)
            cnt = cnt + 1

        resultsFP = []
        for future in futures:
            result = future.result()

            if len(resultsFP) != len(result):
                resultsFP = [0] * len(result)

            for i, val in enumerate(result):
                resultsFP[i] += int(val)


        FScore = [0] * len(resultsTP)
        for i, val in enumerate(resultsTP):
            FScore[i] = 2 * resultsTP[i] / (2 * resultsTP[i] + resultsFP[i] + resultsFN[i])
        
        writer.writerow(FScore)

def calcDetectionFalsePositives(watermark, watermark_name):
    threadPool = ThreadPoolExecutor()

    csvfile = open(watermark_name + "_false_positive.csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

    for detect_level in levels:
        directory = os.fsencode("images/")

        print("level: " + str(detect_level))

        futures = []
        cnt = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            future = threadPool.submit(calcDetectionFalsePositive, watermark, filename, detect_level)
            futures.append(future)
            cnt = cnt + 1

        results = []
        for future in futures:
            result = future.result()

            if len(results) != len(result):
                results = [0] * len(result)

            for i, val in enumerate(result):
                results[i] += int(val)

        for i, val in enumerate(results):
            results[i] = results[i] / cnt

        writer.writerow(results)

def test_watermark(watermark, watermark_name):
    createReferences(watermark)
    calcDetectionThresholds(watermark, watermark_name)


#test_watermark(e_perc_shape, "e_perc_shape")
#test_watermark(dct_watermark, "dct_watermark")
test_watermark(eblind_dlc, "eblind_dlc")
