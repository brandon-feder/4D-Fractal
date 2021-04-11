from math import *
import numpy as np
import quaternion

# ====== SETTINGS ======
MAX_DEPTH = 25
ESCAPE_RADIUS = 4
SIZE = 500
SCALE = 2
mandelbrot=True

if mandelbrot:
    def F1( C, t ):
        return np.quaternion(0, 0, 0, 0), { "C":C }

    def FN(Z, t, variables):
        return Z*Z + variables["C"], variables
else:
    def F1( C, t ):
        return C, { "C":C, "D":np.quaternion(sin(t/20), cos(t/20), sin(t/20), cos(t/20))/2 }

    def FN(Z, t, variables):
        return Z*Z + variables["D"], variables

def ANGLES(t):
    return [
        t/20, t/20, t/20, t/20, t/20, t/20
    ]

FRAMES=320

N_PROCESSES = 8

VIDEO_NAME="fractal"
FPS=16

convert="linear"


"""Convert options:

binary
linear
logarithmic
expontial

"""

COLORMETHOD="escapeTime"

"""COLORMETHOD  options:

escapeTime
averageOrbitDistance
averageOrbitRotation
"""

InColor1=[0, 0, 0, 255]
InColor2=[255, 0, 0, 255]
OutColor1=[255, 255, 255, 255]
OutColor2=[50, 100, 170, 255]

interpRange=InColor1+InColor2+OutColor1+OutColor2

USE_PROCESSES = True
