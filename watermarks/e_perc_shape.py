import subprocess

eperc_shape_exe = "D:/projects/watermarks/project/apps/RelWithDebInfo/e_perc_shape.exe"

#levels = [0.005, 0.006, 0.007, 0.0085, 0.01, 0.0135, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.085, 0.1, 0.11, 0.12, 0.135, 0.15, 0.175, 0.2, 0.225, 0.25, 0.3]
levels = [0.01, 0.02, 0.035, 0.05, 0.065, 0.085, 0.1, 0.13, 0.15, 0.19, 0.22, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.12, 1.25, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5]
detection_levels = [0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.0325, 0.035, 0.0375, 0.04, 0.0425, 0.045, 0.0475, 0.05, 0.0525, 0.055, 0.0575, 0.06, 0.0625, 0.065, 0.0675, 0.07, 0.0725, 0.075]
#detection_levels = [0.00025, 0.0005, 0.00075, 0.001, 0.00125, 0.0015, 0.00175, 0.002, 0.00225, 0.0025, 0.00275, 0.003, 0.00325, 0.0035, 0.00375, 0.004, 0.00425, 0.0045, 0.00475, 0.005, 0.00525, 0.0055, 0.00575, 0.006, 0.00625, 0.0065, 0.00675, 0.007, 0.00725, 0.0075]
#detection_levels = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.10, 0.105, 0.10, 0.115, 0.11, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145]
#detection_levels = [0.000025, 0.00005, 0.000075, 0.0001, 0.000125, 0.00015, 0.000175, 0.0002, 0.000225, 0.00025, 0.000275, 0.0003, 0.000325, 0.00035, 0.000375, 0.0004, 0.000425, 0.00045, 0.000475, 0.0005, 0.000525, 0.00055, 0.000575, 0.0006, 0.000625, 0.00065, 0.000675, 0.0007, 0.000725, 0.00075]

#detection_levels = [0.000625,0.00125,0.001875,0.0025,0.003125,0.00375,0.004375,0.005,0.005625,0.00625,0.006875,0.0075,0.008125,0.00875,0.009375,0.01,0.010625,0.01125,0.011875,0.0125,0.013125,0.01375,0.014375,0.015,0.015625,0.01625,0.016875,0.0175,0.018125,0.01875]


def gen_reference(path_source, path_output, level):
    subprocess.call([eperc_shape_exe, "--gen_reference", "--strength=" + str(levels[level]), "--in=" + path_source, "--out=" + path_output])

def embed(path_source, path_reference, path_output):
    subprocess.call([eperc_shape_exe, "--embed", "--in=" + path_source, "--reference=" + path_reference, "--out=" + path_output])

def detect(path, path_reference, path_origin, threshold_level=-1):
    exe_params = [eperc_shape_exe, "--detect", "--in=" + path, "--reference=" + path_reference, "--origin=" + path_origin]
    if threshold_level != -1:
        exe_params.append("--threshold=" + str(detection_levels[threshold_level]))

    out = subprocess.run(exe_params, capture_output=True, text=True)

    if "TRUE" in out.stdout:
        return True
    else:
        return False

def detect_threshold(path, path_reference, path_origin, threshold):
    exe_params = [eperc_shape_exe, "--detect", "--in=" + path, "--reference=" + path_reference, "--origin=" + path_origin]
    exe_params.append("--threshold=" + str(threshold))
    out = subprocess.run(exe_params, capture_output=True, text=True)

    if "TRUE" in out.stdout:
        return True
    else:
        return False

def get_correlation(path, path_reference, path_origin):
    exe_params = [eperc_shape_exe, "--get_correlation", "--in=" + path, "--reference=" + path_reference, "--origin=" + path_origin]
    out = subprocess.run(exe_params, capture_output=True, text=True)

    return float(out.stdout)


if __name__ == "__main__":
    gen_reference("agriculture-hd.jpg", "reference.bmp", 10)
    embed("agriculture-hd.jpg", "reference.bmp", "watermarked.png")
    print(detect("watermarked.png", "reference.bmp", "agriculture-hd.jpg"))
    print(detect("agriculture-hd.jpg", "reference.bmp", "agriculture-hd.jpg"))

    print(get_correlation("watermarked.png", "reference.bmp", "agriculture-hd.jpg"))
    print(get_correlation("agriculture-hd.jpg", "reference.bmp", "agriculture-hd.jpg"))
