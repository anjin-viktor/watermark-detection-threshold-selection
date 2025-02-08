import subprocess

eblind_exe = "D:/projects/watermarks/project/apps/RelWithDebInfo/eblind_dlc_dctdniz_robust.exe"

levels = [1, 2, 3, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

def gen_reference(path_source, path_output, level, robustness_threshold):
    subprocess.call([eblind_exe, "--gen_reference", "--reference_max=" + str(levels[level]), "--robustness_threshold=" + str(robustness_threshold), "--in=" + path_source, "--out=" + path_output])

def embed(path_source, path_reference, path_output):
    subprocess.call([eblind_exe, "--embed", "--in=" + path_source, "--reference=" + path_reference, "--out=" + path_output, "--alpha=1.0"])

def detect(path, path_reference):
    out = subprocess.run([eblind_exe, "--detect", "--in=" + path, "--reference=" + path_reference], capture_output=True, text=True)
    if "TRUE" in out.stdout:
        return True
    else:
        return False

if __name__ == "__main__":
    gen_reference("agriculture-hd.jpg", "reference.bmp", 7, 30)
    embed("agriculture-hd.jpg", "reference.bmp", "watermarked.png")
    print(detect("watermarked.png", "reference.bmp"))
    print(detect("agriculture-hd.jpg", "reference.bmp"))
