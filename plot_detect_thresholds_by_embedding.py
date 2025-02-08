# -*- coding: cp1251 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys
import math

from matplotlib import cm
import csv
from array import array

Xv = []
detect = []
Headers = []

idx = 0

if len(sys.argv) != 2:
    print("`path_to_csv` argument expected")
    exit(1)

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        detect.append(float(row[1]))
        idx += 1

detect = np.array(detect)
fig, ax = plt.subplots(1, 1)
X = [0.000625, 0.00075, 0.000875, 0.00105, 0.00125, 0.0015, 0.001875, 0.0022, 0.0025, 0.0028, 0.003125, 0.0034375, 0.00375, 0.004375, 0.005, 0.005625, 0.00625, 0.0075, 0.00875, 0.010625, 0.0125, 0.01375, 0.015, 0.016875, 0.01875, 0.021875, 0.025, 0.028125, 0.03125, 0.0375]

#Piva, Alessandro, et al. "Threshold selection for correlation-based watermark detection." Proceedings of COST. Vol. 254. 1998.
Tp1 = []
for x in X:
    Tp = 127 * x / 3
    Tp1.append(Tp)
Tp1 = np.array(Tp1)
print(Tp1)

sigmaSqr = 0
#for i in range(0,256):
#    v = i / 256;
#    val = v * v / 256
#    sigmaSqr += val
#print(sigmaSqr)

Tp2 = []
n = 7626 * (64 - 8) #2542 average size of image in 8x8 blocks
for x in X:
    TP = 2 * (1 + x * x) * sigmaSqr
    TP = TP / n
    TP = math.sqrt(TP)
    Tp = 3.3 * TP
    Tp2.append(Tp)
Tp2 = np.array(Tp2)
#print(Tp2)


ax.plot(X, detect)
#ax.plot(X, Tp1)
#ax.plot(X, Tp2)

ax.set_ylabel('Watermark detection threshold')
ax.set_xlabel('Value of \u03B1 watermark embedding coefficient')
ax.legend(["Detected", "Tp", "T'p"])


plt.show()
