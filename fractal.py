from matplotlib import pyplot as plt
from math import *
import numpy as np
import cmath
import quaternion

from presets import *
from quadmap import *

def quatDist(A, B):
    A1, A2, A3, A4 = A.w, A.x, A.y, A.z
    B1, B2, B3, B4 = B.w, B.x, B.y, B.z

    return sqrt( (A1-B1)**2 + (A2 - B2)**2 + (A3-B3)**2 + (A4-B4)**2 )

# ======== CODE ========
class Coordinate:
    def __init__(self, C, t):
        Z, variables = F1( C, t )
        self.orbit = [ Z ]

        for t in range( MAX_DEPTH ):
            Z, variables = FN(Z, t, variables)
            self.orbit.append( Z )

            if quatDist(Z, C) > ESCAPE_RADIUS:
                self.isInSet = False
                return

        self.isInSet = True

    def getEscapeTime(self):
        return len(self.orbit)

    def getAverageOrbitDistance(self):
        dist = 0
        for o in self.orbit:
            dist += quatDist(o, np.quaternion(0, 0, 0, 0))

        return dist/self.getEscapeTime()

    def getAverageComponents(self):
        w, x, y, z = 0, 0, 0, 0

        for o in self.orbit:
            w += o.w
            x += o.x
            y += o.y
            z += o.z

        w /= self.getEscapeTime()+1
        x /= self.getEscapeTime()+1
        y /= self.getEscapeTime()+1
        z /= self.getEscapeTime()+1

        return w, x, y, z

    def getAverageOrbitRotation(self):
        rX, rY, rZ = 0, 0, 0
        for o in self.orbit:
            rot = o.axis
            rX += rot[0]
            rY += rot[1]
            rZ += rot[2]

        return rX/self.getEscapeTime(), rY/self.getEscapeTime(), rZ/self.getEscapeTime()


class Fractal:
    @staticmethod
    def __isRightAngle(A, B, C):

        left = quatDist(A, B)**2 + quatDist(B, C)**2
        right = quatDist(A, C)**2

        return round( left*10000 ) == round( right*10000 )

    @staticmethod
    def calculate(t):
        A, B, C, D = Quadrilateral.combineRotation(
            ANGLES(t)
        )

        A = np.quaternion(A[0], A[1], A[2], A[3])*SCALE
        B = np.quaternion(B[0], B[1], B[2], B[3])*SCALE
        C = np.quaternion(C[0], C[1], C[2], C[3])*SCALE
        D = np.quaternion(D[0], D[1], D[2], D[3])*SCALE

        if (
            Fractal.__isRightAngle(A, B, C) and
            Fractal.__isRightAngle(B, C, D) and
            Fractal.__isRightAngle(C, D, A)
        ):

            dx = (C - B)/SIZE
            dy = (A - B)/SIZE

            coords = [ [ None for _ in range(SIZE) ] for _ in range(SIZE) ]

            for x in range(SIZE):
                print(x/SIZE)
                for y in range(SIZE):
                    coords[x][y] = Coordinate( B + dx*x + dy*y, t )

            return coords

        else:
            print("Do not form right angle")
            exit()
