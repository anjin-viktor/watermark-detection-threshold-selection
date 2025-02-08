from utils import detect_threshold

def calcScores(watermark_name, ebmedding_level, min, max):
    thresholds = detect_threshold.extractThresholds(detect_threshold.getThresholdsFilename(watermark_name, ebmedding_level))
    detect_threshold.calcFScoreGraph(thresholds, detect_threshold.getScoresFilename(watermark_name, ebmedding_level), min, max)

### Script uses calculated threshold from file created by find_detect_thredhold_calc_correlations.py
ebmedding_level = 7
calcScores("eblind_dlc", 7, 0, 0.01)
#ebmedding_level = 12
calcScores("eblind_dlc", 12, 0, 0.01)
#ebmedding_level = 20
calcScores("eblind_dlc", 20, 0, 0.01)

#ebmedding_level = 5
#calcScores("dct_watermark", 5, 0, 0.1)
#ebmedding_level = 10
#calcScores("dct_watermark", 10, 0, 0.1)
#ebmedding_level = 17
#calcScores("dct_watermark", 17, 0, 0.1)
