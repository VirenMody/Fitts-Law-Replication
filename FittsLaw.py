from graphics import *
from graphicsexamples import *
import math


# checks where use clicked in target
def clickedInTarget(clickedPoint, target):
    # get the distance from clicked point to the circle center
    xDist = clickedPoint.getX() - target.getCenter().getX()
    yDist = clickedPoint.getY() - target.getCenter().getY()
    distance = math.sqrt(xDist*xDist + yDist*yDist)

    return distance <= target.getRadius()

def main():
    xMax = yMax = 500
    distance = 400
    radius = distance/2
    width = 50
    numTargets = 20
    degreesBetweenTargets = 360/numTargets

    # Create graphical window and center origin
    win = GraphWin("Fitts' Law", xMax, yMax)
    win.setBackground("white")
    win.setCoords(-249, -249, 249, 249)

    # Center circle
    c = Circle(Point(0, 0), 10)
    c.setFill("blue")
    c.draw(win)

    circleList = []

    # Draw circle of circles
    for i in range(0, numTargets):
        xCenter = radius*(math.cos(math.radians(degreesBetweenTargets*i)))
        yCenter = radius*(math.sin(math.radians(degreesBetweenTargets*i)))

        print ('Iteration: ', i,' --> ', xCenter, ', ', yCenter)
        c = Circle(Point(xCenter, yCenter), width/2)
        c.setOutline("gray")
        circleList.append(c)

    startTarget = circleList[0]
    endTarget = circleList[10]
    startTarget.setFill("red")

    for circle in circleList:
        circle.draw(win)

    clickedPoint = win.getMouse()
    target = startTarget
    if clickedInTarget(clickedPoint, target):
        print('You did it!!!!!')


    #exit
    win.getMouse() # pause for click in window
    win.close()


main()
