import subprocess

dct_watermark_exe = "D:/projects/watermarks/project/apps/RelWithDebInfo/dct_watermark.exe"

levels = [0.000625, 0.00075, 0.000875, 0.00105, 0.00125, 0.0015, 0.001875, 0.0022, 0.0025, 0.0028, 0.003125, 0.0034375, 0.00375, 0.004375, 0.005, 0.005625, 0.00625, 0.0075, 0.00875, 0.010625, 0.0125, 0.01375, 0.015, 0.016875, 0.01875, 0.021875, 0.025, 0.028125, 0.03125, 0.0375]
#levels = [1, 2, 3, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
#detection_levels = [0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.0325, 0.035, 0.0375, 0.04, 0.0425, 0.045, 0.0475, 0.05, 0.0525, 0.055, 0.0575, 0.06, 0.0625, 0.065, 0.0675, 0.07, 0.0725, 0.075]
detection_levels = [0.00025, 0.0005, 0.00075, 0.001, 0.00125, 0.0015, 0.00175, 0.002, 0.00225, 0.0025, 0.00275, 0.003, 0.00325, 0.0035, 0.00375, 0.004, 0.00425, 0.0045, 0.00475, 0.005, 0.00525, 0.0055, 0.00575, 0.006, 0.00625, 0.0065, 0.00675, 0.007, 0.00725, 0.0075]
dct_skip = 8


def gen_reference(path_source, path_output, level):
    subprocess.call([dct_watermark_exe, "--gen_reference", "--reference_max=255", "--skip_count=" + str(dct_skip), "--in=" + path_source, "--out=" + path_output])
# 
def embed(path_source, path_reference, path_output, level):
    subprocess.call([dct_watermark_exe, "--embed", "--barni=true", "--in=" + path_source, "--reference=" + path_reference, "--out=" + path_output, "--skip_count=" + str(dct_skip), "--alpha="+ str(levels[level])])

def detect(path, path_reference, path_origin, threshold_level=-1):
    exe_params = [dct_watermark_exe, "--detect", "--in=" + path, "--reference=" + path_reference, "--skip_count=" + str(dct_skip)]
    if threshold_level != -1:
        exe_params.append("--threshold=" + str(detection_levels[threshold_level]))

    out = subprocess.run(exe_params, capture_output=True, text=True)

    if "TRUE" in out.stdout:
        return True
    else:
        return False

def detect_threshold(path, path_reference, path_origin, threshold):
    exe_params = [dct_watermark_exe, "--detect", "--in=" + path, "--reference=" + path_reference, "--skip_count=" + str(dct_skip)]
    exe_params.append("--threshold=" + str(threshold))
    out = subprocess.run(exe_params, capture_output=True, text=True)

    if "TRUE" in out.stdout:
        return True
    else:
        return False

def get_correlation(path, path_reference, path_origin):
    exe_params = [dct_watermark_exe, "--get_correlation", "--in=" + path, "--reference=" + path_reference, "--skip_count=" + str(dct_skip)]
    out = subprocess.run(exe_params, capture_output=True, text=True)

    correlcation = 0
    try:
        correlcation = float(out.stdout)
    except ValueError:
        correlcation = 0

    return correlcation



if __name__ == "__main__":
    gen_reference("agriculture-hd.jpg", "reference.bmp", 1)
    embed("agriculture-hd.jpg", "reference.bmp", "watermarked.png", 1)
    print(detect("watermarked.png", "reference.bmp", "agriculture-hd.jpg"))
    print(detect("agriculture-hd.jpg", "reference.bmp", "agriculture-hd.jpg"))

    print(get_correlation("watermarked.png", "reference.bmp", "agriculture-hd.jpg"))
    print(get_correlation("agriculture-hd.jpg", "reference.bmp", "agriculture-hd.jpg"))
