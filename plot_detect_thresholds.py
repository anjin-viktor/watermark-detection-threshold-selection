# -*- coding: cp1251 -*-
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import cm
import csv
from array import array

Xv = []
Yv = []
results = []
idx = 1

if len(sys.argv) != 2:
    print("`path_to_csv` argument expected")
    exit(1)

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
       results.append(row)
       Xv.append(idx)
       Yv.append(idx)
       idx += 1

Z = np.array(results)
plt.style.use('_mpl-gallery')


X, Y = np.meshgrid(Xv, Yv)

# Plot the surface
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(X, Y, Z)

ax.set_ylabel('')
ax.set_xlabel('')
ax.set_zlabel('detection probability')

ax.yaxis.get_major_locator().set_params(integer=True)
ax.xaxis.get_major_locator().set_params(integer=True)

plt.show()
