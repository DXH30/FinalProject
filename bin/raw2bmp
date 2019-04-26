#!/usr/bin/python2
import numpy as np
from matplotlib import pylab as plt
import os
import array
import sys

if (len(sys.argv) < 2):
    print("Usage: %s %s %s" % (sys.argv[0], "filein.raw", "fileout.png"));
    sys.exit()
else:
    filename = sys.argv[1];
    fileout = sys.argv[2];
    f = open(filename, 'rb');
    ln = os.path.getsize(filename);
    width = 250;
    rem = ln%width;
    a = array.array("B");
    a.fromfile(f, ln-rem);
    f.close();
    height = np.uint16(len(a)/width);
    g = np.reshape(a,(height,width));
    g = np.uint8(g);

    plt.imsave(fileout,g,dpi=900);
