from math import *
import numpy as np

class Quadrilateral:
    @staticmethod
    def map2D(): #angle is in radians
        point1=np.array([1, 1, 0, 0])
        point2=np.array([-1, 1, 0, 0])
        point3=np.array([-1, -1, 0, 0])
        point4=np.array([1, -1, 0, 0])

        return point1, point2, point3, point4

    @staticmethod
    def __multiplyMatricies(point1, point2, point3, point4, matrix):
        return np.matmul(matrix, point1), np.matmul(matrix, point2), np.matmul(matrix, point3), np.matmul(matrix, point4)

    @staticmethod
    def __zwRotation(angle, point1, point2, point3, point4):
        zwAxisRotation=np.array([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        return Quadrilateral.__multiplyMatricies(point1, point2, point3, point4, zwAxisRotation)

    @staticmethod
    def __ywRotation(angle, point1, point2, point3, point4):
        ywAxisRotation=np.array([
            [cos(angle), 0, -sin(angle), 0],
            [0, 1, 0, 0],
            [sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

        return Quadrilateral.__multiplyMatricies(point1, point2, point3, point4, ywAxisRotation)

    @staticmethod
    def __yzRotation(angle, point1, point2, point3, point4):
        yzAxisRotation=np.array([
            [cos(angle), 0, 0, -sin(angle)],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [sin(angle), 0, 0, cos(angle)]
        ])

        return Quadrilateral.__multiplyMatricies(point1, point2, point3, point4, yzAxisRotation)

    @staticmethod
    def __xwRotation(angle, point1, point2, point3, point4):
        xwAxisRotation=np.array([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])

        return Quadrilateral.__multiplyMatricies(point1, point2, point3, point4, xwAxisRotation)

    @staticmethod
    def __xzRotation(angle, point1, point2, point3, point4):
        xzAxisRotation=np.array([
            [1, 0, 0, 0],
            [0, cos(angle), 0, -sin(angle)],
            [0, 0, 1, 0],
            [0, sin(angle), 0, cos(angle)]
        ])

        return Quadrilateral.__multiplyMatricies(point1, point2, point3, point4, xzAxisRotation)

    @staticmethod
    def __xyRotation(angle, point1, point2, point3, point4):
        xyAxisRotation=np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos(angle), -sin(angle)],
            [0, 0, sin(angle), cos(angle)]
        ])

        return Quadrilateral.__multiplyMatricies(point1, point2, point3, point4, xyAxisRotation)

    @staticmethod
    def combineRotation(angleList):
        A, B, C, D=Quadrilateral.map2D()

        A, B, C, D=Quadrilateral.__zwRotation(angleList[0], A, B, C, D)
        A, B, C, D=Quadrilateral.__ywRotation(angleList[1], A, B, C, D)
        A, B, C, D=Quadrilateral.__yzRotation(angleList[2], A, B, C, D)
        A, B, C, D=Quadrilateral.__xwRotation(angleList[3], A, B, C, D)
        A, B, C, D=Quadrilateral.__xzRotation(angleList[4], A, B, C, D)
        A, B, C, D=Quadrilateral.__xyRotation(angleList[5], A, B, C, D)

        return A, B, C, D
