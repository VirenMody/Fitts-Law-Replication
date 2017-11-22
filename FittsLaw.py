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
    userData = pd.DataFrame(columns=['User', 'Case', 'Target Width', 'Amplitude', 'ID', 'Movement Time', 'Throughput'])
    windowSize = 800
    xyMax = windowSize / 2 - 1
    xyMin = -1 * xyMax

    numTargets = 16
    targetWidths = [55]
    amplitudes = [400]
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

    for x in range(0, 2):
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
            displayParameters = Text(Point(-300, -300), paramString)
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
                           'Throughput': id/movementTime}]
                userData = userData.append(data)

            # Clear the window, undraw circle of all circles
            for circle in circleList:
                circle.undraw()
            displayParameters.undraw()


    print(userData)
    sortedUserData = userData.sort_values(by='ID')
    userData.to_csv('UserData.csv')


    averagedData = sortedUserData.groupby(['ID'])['Movement Time', 'Throughput'].mean().reset_index()
    print(averagedData)
    averagedData.to_csv('AveragedData.csv')

    # data analysis for MT over ID *********************
    xID = averagedData['ID'].values[:, np.newaxis]
    yMT = averagedData['Movement Time'].values

    xMin = math.floor(averagedData['ID'].min())
    xMax = math.ceil(averagedData['ID'].max())
    yMin = math.floor(averagedData['Movement Time'].min())
    yMax = math.ceil(averagedData['Movement Time'].max())

    linRegModelMT = linear_model.LinearRegression()
    linRegModelMT.fit(xID, yMT)
    # The coefficients
    firstSlope = linRegModelMT.coef_
    firstIntercept = linRegModelMT.intercept_
    domainVal = np.arange(0, xMax+1)
    line = firstSlope*domainVal + firstIntercept
    print('Coefficients for MT over ID:')
    print('Slope: \n', linRegModelMT.coef_)
    print('Intercept: \n', linRegModelMT.intercept_)

    plt.figure(1)
    pylab.title('Linear Regression of Movement Time (MT) over Index of Difficulty (IT)')
    plt.ylabel('Movement Time (seconds)')
    plt.xlabel('Index of Difficulty (bits)')
    plt.axis([0, xMax, 0, yMax])
    plt.xticks(np.arange(0, xMax+0.5, 0.5))
    plt.yticks(np.arange(0, yMax+0.25, 0.25))
    plt.scatter(xID, yMT, color='black')
    plt.plot(domainVal, line)
    ax = plt.gca()
    ax.set_axis_bgcolor((0.898, 0.898, 0.898))

    # data analysis for TP over ID *********************
    xID = averagedData['ID'].values[:, np.newaxis]
    yTP = averagedData['Throughput'].values

    xMin = math.floor(averagedData['ID'].min())
    xMax = math.ceil(averagedData['ID'].max())
    yMin = math.floor(averagedData['Throughput'].min())
    yMax = math.ceil(averagedData['Throughput'].max())

    linRegModelTP = linear_model.LinearRegression()
    linRegModelTP.fit(xID, yTP)
    # The coefficients
    secondSlope = linRegModelTP.coef_
    secondIntercept = linRegModelTP.intercept_
    domainVal = np.arange(0, xMax+1)
    line2 = secondSlope*domainVal + secondIntercept
    print('Coefficients for TP over ID:')
    print('Slope: \n', linRegModelTP.coef_)
    print('Intercept: \n', linRegModelTP.intercept_)

    plt.figure(2)
    pylab.title('Linear Regression of Throughput (TP) over Index of Difficulty (IT)')
    plt.ylabel('Throughput (bits per second)')
    plt.xlabel('Index of Difficulty (bits)')
    plt.axis([0, xMax, 0, yMax])
    plt.xticks(np.arange(0, xMax+0.5, 0.5))
    plt.yticks(np.arange(0, yMax+0.25, 0.25))
    plt.scatter(xID, yTP, color='black')
    plt.plot(domainVal, line2)
    ax = plt.gca()
    ax.set_axis_bgcolor((0.898, 0.898, 0.898))

    plt.show()

    #exit
    win.close()

main()
