from PIL import Image
import numpy as np
import os
import random
from math import log
from multiprocessing import Process

from quadmap import *
from fractal import *
from presets import *

def calcFrame(frame):
    pixels=np.ndarray( (SIZE, SIZE, 4) )
    pixelMagnitude=Fractal.calculate(frame+50)

    print(frame/FRAMES)

    for x in range(SIZE):
        for y in range(SIZE):

            pixels[x][y][0], pixels[x][y][1], pixels[x][y][2], pixels[x][y][3]=Graphics.convert(pixelMagnitude[x][y], interpRange)

    image=Image.fromarray(np.uint8(pixels)).convert('RGB')
    image.save("./data/{}.png".format(frame))

class Graphics:
    @staticmethod
    def convert(Input, InterpRange): #Input is in range [0, Maximum];
    #InterpRange is list with 8 elements
    #magnitudePercent is magnitude of each pixel in scale [0, 1]
        if convert=="binary":
            if Input.isInSet:
                magnitudePercent=1
            else:
                magnitudePercent=0

            Red=int((InterpRange[4]-InterpRange[0])*magnitudePercent+InterpRange[0])
            Green=int((InterpRange[5]-InterpRange[1])*magnitudePercent+InterpRange[1])
            Blue=int((InterpRange[6]-InterpRange[2])*magnitudePercent+InterpRange[2])
            Alpha=int((InterpRange[7]-InterpRange[3])*magnitudePercent+InterpRange[3])

        else:
            if COLORMETHOD=="escapeTime":
                NInput=Input.getEscapeTime()
                Maximum=MAX_DEPTH
            elif COLORMETHOD=="averageOrbitDistance":
                NInput=Input.getAverageOrbitDistance()
                Maximum=NInput+100
            elif COLORMETHOD=="averageComponents":
                averageComp=Input.getAverageComponents()
                Maximum=ESCAPE_RADIUS/5

                # print( averageComp, ESCAPE_RADIUS )

                NInputW=min(abs(averageComp[0]), ESCAPE_RADIUS/2)
                NInputX=min(abs(averageComp[1]), ESCAPE_RADIUS/2)
                NInputY=min(abs(averageComp[2]), ESCAPE_RADIUS/2)

                if convert=="linear":
                    magnitudePercentW=(NInputW)/Maximum
                    magnitudePercentX=(NInputX)/Maximum
                    magnitudePercentY=(NInputY)/Maximum
                elif convert=="logarithmic":
                    magnitudePercentW=(log(NInputW))/log(Maximum)
                    magnitudePercentX=(log(NInputX))/log(Maximum)
                    magnitudePercentY=(log(NInputY))/log(Maximum)

                if Input.isInSet:
                    Red=int((InterpRange[4]-InterpRange[0])*magnitudePercentW+InterpRange[0])
                    Green=int((InterpRange[5]-InterpRange[1])*magnitudePercentY+InterpRange[1])
                    Blue=int((InterpRange[6]-InterpRange[2])*magnitudePercentX+InterpRange[2])
                    Alpha=255
                else:
                    Red=int((InterpRange[12]-InterpRange[8])*magnitudePercentW+InterpRange[8])
                    Green=int((InterpRange[13]-InterpRange[9])*magnitudePercentY+InterpRange[9])
                    Blue=int((InterpRange[14]-InterpRange[10])*magnitudePercentX+InterpRange[10])
                    Alpha=255
                return Red, Green, Blue, Alpha
            if convert=="linear":
                magnitudePercent=(NInput)/Maximum
            elif convert=="logarithmic":
                magnitudePercent=(log(NInput))/log(Maximum)
            elif convert=="expontial":
                magnitudePercent=(10*NInput)/log(Maximum)

            if Input.isInSet:
                Red=int((InterpRange[4]-InterpRange[0])*magnitudePercent+InterpRange[0])
                Green=int((InterpRange[5]-InterpRange[1])*magnitudePercent+InterpRange[1])
                Blue=int((InterpRange[6]-InterpRange[2])*magnitudePercent+InterpRange[2])
                Alpha=int((InterpRange[7]-InterpRange[3])*magnitudePercent+InterpRange[3])
            else:
                Red=int((InterpRange[12]-InterpRange[8])*magnitudePercent+InterpRange[8])
                Green=int((InterpRange[13]-InterpRange[9])*magnitudePercent+InterpRange[9])
                Blue=int((InterpRange[14]-InterpRange[10])*magnitudePercent+InterpRange[10])
                Alpha=int((InterpRange[15]-InterpRange[11])*magnitudePercent+InterpRange[11])

        return Red, Green, Blue, Alpha

    @staticmethod
    def __image(InterpRange):
        if USE_PROCESSES:
            for frame in range(0, FRAMES, N_PROCESSES):
                process = []
                for p in range(N_PROCESSES):
                    process.append( Process( target=calcFrame, args=(frame + p,) ) )
                    process[p].start()

                for p in range(N_PROCESSES):
                    process[p].join()
        else:
            for frame in range(0, FRAMES):
                calcFrame(frame)


    @staticmethod
    def createVideo(InterpRange):
        Graphics.__image(InterpRange)
        os.system("rm ./{}.mov; ffmpeg -framerate {} -start_number 1 -i ./data/%d.png {}.mov".format(VIDEO_NAME, FPS, VIDEO_NAME))
if __name__ ==  '__main__':
    Graphics.createVideo(interpRange)
