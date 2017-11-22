from graphics import *
from graphicsexamples import *
from random import shuffle
import pandas as pd
import itertools
import math
import time
#import xlwt

# checks where use clicked in target
def clickedInTarget(clickedPoint, target):
    # get the distance from clicked point to the circle center
    xDist = clickedPoint.getX() - target.getCenter().getX()
    yDist = clickedPoint.getY() - target.getCenter().getY()
    distance = math.sqrt(xDist*xDist + yDist*yDist)

    return distance <= target.getRadius()

def main():
    userData = pd.DataFrame(columns=['User', 'Case', 'Width', 'Amplitude', 'ID', 'Time'])
    windowSize = 700
    xyMax = windowSize / 2 - 1
    xyMin = -1 * xyMax

    numTargets = 4
    targetWidths = [35, 55]
    amplitudes = [200, 400, 600]
    parameters = list(itertools.product(targetWidths, amplitudes))
    degreesBetweenTargets = 360/numTargets

    # Create graphical window and center origin
    win = GraphWin("Fitts' Law", windowSize, windowSize)
    win.setBackground("white")
    win.setCoords(xyMin, xyMin, xyMax, xyMax)

    # Exit Button


    # Center circle
    c = Circle(Point(0, 0), 10)
    c.setFill("blue")
    c.draw(win)

    userNumber = 0
    collectingData = True
    while collectingData:

        userNumber += 1
        caseNumber = 0
        shuffle(parameters)

        for targetWidth, amplitude in parameters:

            caseNumber += 1
            radius = amplitude / 2
            circleList = []

            paramString = "User Number: " + str(userNumber) + "\n" \
                          "Case Number: " + str(caseNumber) + "\n" \
                          "Target Width: " + str(targetWidth) + " pixels\n" \
                          "Diameter: " + str(amplitude) + " pixels"
            displayParameters = Text(Point(-249, -249), paramString)
            displayParameters.draw(win)

            # Populate circleList with circles of targetWidth and amplitude/diameter
            for i in range(0, numTargets):
                xCenter = radius*(math.cos(math.radians(degreesBetweenTargets*i)))
                yCenter = radius*(math.sin(math.radians(degreesBetweenTargets*i)))

                c = Circle(Point(xCenter, yCenter), targetWidth/2)
                c.setOutline("black")
                c.setFill("gray")
                circleList.append(c)

            # Draw circle of circles
            for circle in circleList:
                circle.draw(win)

            # Loop through all numTarget/2 pairs
            for i in range(0, int(numTargets/2)):
                startTarget = circleList[i]
                endTarget = circleList[i+int(numTargets/2)]
                startTarget.setFill("red")

                targetNotClicked = True
                while targetNotClicked:
                    clickedPoint = win.getMouse()
                    if clickedInTarget(clickedPoint, startTarget):
                        startTime = time.time()
                        startTarget.setFill("gray")
                        endTarget.setFill("red")
                        targetNotClicked = False

                targetNotClicked = True
                while targetNotClicked:
                    clickedPoint = win.getMouse()
                    if clickedInTarget(clickedPoint, endTarget):
                        endTime = time.time()
                        endTarget.setFill("gray")
                        targetNotClicked = False

                movementTime = endTime-startTime

                id = math.log2(amplitude/targetWidth + 1)
                data = [{'User': userNumber,
                           'Case': caseNumber,
                           'Width': targetWidth,
                           'Amplitude': amplitude,
                           'ID': id,
                           'Time': movementTime}]
                userData = userData.append(data)

            # Clear the window, undraw circle of all circles
            for circle in circleList:
                circle.undraw()
            displayParameters.undraw()

        print(userData)
        collectingData = False

    #exit
    win.close()


main()
