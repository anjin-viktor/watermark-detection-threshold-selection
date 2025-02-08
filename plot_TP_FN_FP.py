import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import cm
import csv
from array import array
from matplotlib.ticker import FuncFormatter

Xv = []
idx = 0
X = []
TP = []
TN = []
FP = []
FN = []

cnt = 14 * 8091


if len(sys.argv) != 2:
    print("`path_to_csv` argument expected")
    exit(1)

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)

    idx = 0
    for row in reader:
        if idx == 0:
            for v in row:
                X.append(float(v))
        elif idx == 2:
            for v in row:
                TP.append(float(v) * cnt)
        elif idx == 3:
            for v in row:
                TN.append(float(v) * cnt)
        elif idx == 4:
            for v in row:
                FP.append(float(v) * cnt)
        elif idx == 5:
            for v in row:
                FN.append(float(v) * cnt)

        idx = idx + 1

TP = np.array(TP)
FN = np.array(FN)
FP = np.array(FP)
TN = np.array(TN)
X = np.array(X)


fig, ax = plt.subplots(1, 1)

ax.plot(X, TP)
ax.plot(X, TN)
ax.plot(X, FP)
ax.plot(X, FN)


#ax.set_title("E_BLIND/D_LC, \u03B1=0.059") #e_blind_dlc 7
ax.set_title("E_BLIND/D_CC, \u03B1=0,1") #e_blind_dlc 12
#ax.set_title("E_BLIND/D_LC, \u03B1=0.19") #e_blind_dlc 20

#ax.set_title("DCT-ЦВЗ, \u03B1=0.039") #dct_watermark 5
#ax.set_title("DCT-ЦВЗ, \u03B1=0.086") #dct_watermark 10
#ax.set_title("DCT-ЦВЗ, \u03B1=0.156") #dct_watermark 17


ax.legend(["TP(x)", "TN(x)", "FP(x)", "FN(x)"])
ax.set_ylabel('Количество изображений')
ax.set_xlabel('Пороговое значение обнаружения')

def comma_formatter(x, pos):
    return str(x).replace('.', ',')
 
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))
#plt.yticks([tick for tick in plt.yticks()[0]], [
#           str(tick).replace('.', ',') for tick in plt.yticks()[0]])

plt.show()
