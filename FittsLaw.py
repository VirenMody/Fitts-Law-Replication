from graphics import *
from graphicsexamples import *
import math
import time

# checks where use clicked in target
def clickedInTarget(clickedPoint, target):
    # get the distance from clicked point to the circle center
    xDist = clickedPoint.getX() - target.getCenter().getX()
    yDist = clickedPoint.getY() - target.getCenter().getY()
    distance = math.sqrt(xDist*xDist + yDist*yDist)

    return distance <= target.getRadius()

def main():
    windowSize = 700
    xyMax = windowSize / 2 - 1
    xyMin = -1 * xyMax

    numTargets = 20
    targetWidths = [25, 45]
    diameters = [200, 300, 400]
    degreesBetweenTargets = 360/numTargets

    # Create graphical window and center origin
    win = GraphWin("Fitts' Law", windowSize, windowSize)
    win.setBackground("white")
    win.setCoords(xyMin, xyMin, xyMax, xyMax)

    for targetWidth in targetWidths:

        for diameter in diameters:
            # Center circle
            c = Circle(Point(0, 0), 10)
            c.setFill("blue")
            c.draw(win)

            radius = diameter / 2
            circleList = []

            # Populate circleList with circles of targetWidth and diameter/amplitude
            for i in range(0, numTargets):
                xCenter = radius*(math.cos(math.radians(degreesBetweenTargets*i)))
                yCenter = radius*(math.sin(math.radians(degreesBetweenTargets*i)))

                print ('Iteration: ', i,' --> ', xCenter, ', ', yCenter)
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
                        print('You got the START!!')
                        startTarget.setFill("gray")
                        endTarget.setFill("red")
                        targetNotClicked = False

                targetNotClicked = True
                while targetNotClicked:
                    clickedPoint = win.getMouse()
                    if clickedInTarget(clickedPoint, endTarget):
                        endTime = time.time()
                        print('You got the END!!!')
                        endTarget.setFill("gray")
                        targetNotClicked = False

                print(endTime-startTime)

            # Clear the window, undraw circle of all circles
            for circle in circleList:
                circle.undraw()

    #exit
    win.close()


main()
