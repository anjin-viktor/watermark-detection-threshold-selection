import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.ticker import FuncFormatter


from matplotlib import cm
import csv
from array import array

X = []
Xv = []
idx = 0
FScores = []
TP = []
TN = []
FP = []
FN = []


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
        if idx == 1:
            for v in row:
                FScores.append(float(v))
        elif idx == 2:
            for v in row:
                TP.append(float(v))
        elif idx == 3:
            for v in row:
                TN.append(float(v))
        elif idx == 4:
            for v in row:
                FP.append(float(v))
        elif idx == 5:
            for v in row:
                FN.append(float(v))

        idx = idx + 1

FScores = np.array(FScores)
FN = np.array(FN)
FP = np.array(FP)

fig, ax = plt.subplots(1, 1)
X = np.array(X)

ax.plot(X, FScores)
#ax.plot(X, FN)
#ax.plot(X, FP)


#ax.set_title("E_BLIND/D_CC, \u03B1=0,059") #e_blind_dlc 7
#ax.set_title("E_BLIND/D_CC, \u03B1=0,1") #e_blind_dlc 12
ax.set_title("E_BLIND/D_CC, \u03B1=0,19") #e_blind_dlc 20

#ax.set_title("ДКП-ЦВЗ, \u03B1=0,039") #dct_watermark 5
#ax.set_title("ДКП-ЦВЗ, \u03B1=0,086") #dct_watermark 10
#ax.set_title("ДКП-ЦВЗ, \u03B1=0,156") #dct_watermark 17


#ax.legend(["F-мера", "FN / число изображений", "FP / число изображений"])
ax.legend(["F-мера"])
#ax.set_ylabel('')
plt.xlabel('Пороговое значение обнаружения')
plt.ylabel('Величина F-меры')

xmax = X[np.argmax(FScores)]
ymax = FScores.max()

plt.plot(xmax,ymax,'s')
plt.axvline(xmax, ls=':', c='k')
plt.text(xmax, ymax*0.95, f'({round(xmax,4)}, {round(ymax,4)})')

def comma_formatter(x, pos):
    return str(x).replace('.', ',')
 
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))


plt.show()
