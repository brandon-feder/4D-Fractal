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
        return np.quaternion(0, 0, 0, 0), { "C":1/C if not C == np.quaternion(0, 0, 0, 0) else 0 }

    def FN(Z, t, variables):
        return Z*Z + variables["C"], variables
else:
    def F1( C, t ):
        return C, { "C":C, "D":np.quaternion(sin(t/20), cos(t/20), sin(t/20), cos(t/20))/2 }

    def FN(Z, t, variables):
        return Z*Z + variables["D"], variables

def ANGLES(t):
    return [
        t/10, t/10, t/18, t/20, t/91, t/20
    ]

FRAMES=640

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

COLORMETHOD="averageComponents"

"""COLORMETHOD  options:

escapeTime
averageOrbitDistance
averageComponents
"""

OutColor1=[153, 0, 76, 255]
OutColor2=[0, 204, 0, 255]
InColor1=[255, 255, 255, 255]
InColor2=[240, 240, 240, 255]

interpRange=InColor1+InColor2+OutColor1+OutColor2

USE_PROCESSES = True
