import numpy as np
from matplotlib import pylab as plt
import os
import array
import time
import sys

mypath = "./"
plt.figure()
for i in range(1,100):
    num = "%03d" % i;
    try:
        filename = mypath+"payload.log."+num
        f = open(filename, 'rb')
        ln = os.path.getsize(filename)
        width = 250
        rem = ln%width
        a = array.array("B")
        a.fromfile(f,ln-rem)
        f.close()
        height = np.uint16(len(a)/width)
        g = np.reshape(a,(height,width))
        g = np.uint8(g)
        plt.imshow(g)
        plt.draw()
    except Exception as ex:
        print(ex)
