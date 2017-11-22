from graphics import *
from graphicsexamples import *
from random import shuffle
import pandas as pd
import itertools
import math
import time

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from matplotlib import pylab


# checks where use clicked in target
def clickedInTarget(clickedPoint, target):
    # get the distance from clicked point to the circle center
    xDist = clickedPoint.getX() - target.getCenter().getX()
    yDist = clickedPoint.getY() - target.getCenter().getY()
    distance = math.sqrt(xDist*xDist + yDist*yDist)

    return distance <= target.getRadius()

def main():
    userData = pd.DataFrame(columns=['User', 'Case', 'Target Width', 'Amplitude', 'ID', 'Movement Time', 'TP'])
    windowSize = 700
    xyMax = windowSize / 2 - 1
    xyMin = -1 * xyMax

    numTargets = 2
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
    # c = Circle(Point(0, 0), 10)
    # c.setFill("blue")
    # c.draw(win)

    userNumber = 0

    for x in range(0, 1):
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
                           'Target Width': targetWidth,
                           'Amplitude': amplitude,
                           'ID': id,
                           'Movement Time': movementTime,
                           'TP': id/movementTime}]
                userData = userData.append(data)

            # Clear the window, undraw circle of all circles
            for circle in circleList:
                circle.undraw()
            displayParameters.undraw()


    print(userData)
    sortedUserData = userData.sort_values(by='ID')
    print(sortedUserData)

    # data analysis for MT over ID *********************
    xID = userData['ID'].values[:, np.newaxis]
    yMT = userData['Movement Time'].values

    xMin = math.floor(userData['ID'].min())
    xMax = math.ceil(userData['ID'].max())
    yMin = math.floor(userData['Movement Time'].min())
    yMax = math.ceil(userData['Movement Time'].max())


    linRegModel = linear_model.LinearRegression()
    linRegModel.fit(xID, yMT)
    # The coefficients
    firstSlope = linRegModel.coef_
    firstIntercept = linRegModel.intercept_
    domainVal = np.arange(0, xMax+1)
    line = firstSlope*domainVal + firstIntercept
    print('Coefficients: \n', linRegModel.coef_)
    print('Intercept: \n', linRegModel.intercept_)
    plt.figure(0)
    pylab.title('Linear Regression of Movement Time (MT) over Index of Difficulty (IT)')
    plt.ylabel('Movement Time (seconds)')
    plt.xlabel('Index of Difficulty (bits)')
    plt.axis([0, xMax, 0, yMax])
    plt.xticks(np.arange(0, xMax+0.5, 0.5))
    plt.yticks(np.arange(0, yMax+0.25, 0.25))
    plt.scatter(xID, yMT, color='black')
    plt.plot(domainVal, line)
    ax = plt.gca()
    # ax.set_axis_bgcolor((0.898, 0.898, 0.898))
    plt.show()

    # data analysis for TP over ID *********************
    # xID = userData['ID'].values[:, np.newaxis]
    yTP = userData['TP'].values

    xMin = math.floor(userData['ID'].min())
    xMax = math.ceil(userData['ID'].max())
    yMin = math.floor(userData['TP'].min())
    yMax = math.ceil(userData['TP'].max())

    linRegModel = linear_model.LinearRegression()
    linRegModel.fit(xID, yTP)
    # The coefficients
    secondSlope = linRegModel.coef_
    secondIntercept = linRegModel.intercept_
    domainVal = np.arange(0, xMax+1)
    line2 = secondSlope*domainVal + secondIntercept
    print('Coefficients: \n', linRegModel.coef_)
    print('Intercept: \n', linRegModel.intercept_)
    plt.figure(1)
    pylab.title('Linear Regression of Throughput (TP) over Index of Difficulty (IT)')
    plt.ylabel('Throughput (bits per second)')
    plt.xlabel('Index of Difficulty (bits)')
    plt.axis([0, xMax, 0, yMax])
    plt.xticks(np.arange(0, xMax+0.5, 0.5))
    plt.yticks(np.arange(0, yMax+0.25, 0.25))
    plt.scatter(xID, yMT, color='black')
    plt.plot(domainVal, line2)
    ax = plt.gca()
    ax.set_axis_bgcolor((0.898, 0.898, 0.898))
    plt.show()
    win.getMouse()


    #exit
    win.getMouse()
    win.close()


main()
