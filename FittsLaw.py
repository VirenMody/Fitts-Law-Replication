from graphics import *
from graphicsexamples import *
import math

def main():
    xMax = yMax = 500
    center = xMax/2 - 1
    distance = 400
    radius = distance/2
    width = 50
    numTargets = 20


    win = GraphWin("Fitts' Law", xMax, yMax)
    win.setBackground("white")
    win.setCoords(-249, -249, 249, 249)


    c = Circle(Point(0, 0), 10)
    c.setFill("blue")
    c.draw(win)

    circleList = []

    for x in range(0, numTargets):
        xCenter = radius*(math.cos(math.radians(18*x)))
        yCenter = radius*(math.sin(math.radians(18*x)))

        print ('Iteration: ', x,' --> ', xCenter, ', ', yCenter)
        c = Circle(Point(xCenter, yCenter), width/2)
        c.setOutline("gray")
        circleList.append(c)

    for circle in circleList:
        circle.draw(win)
    win.getMouse() # pause for click in window
    win.close()


main()