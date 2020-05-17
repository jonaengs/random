import turtle

# https://realpython.com/beginners-guide-python-turtle/

s = turtle.getscreen()
t = turtle.Turtle()
t.speed(5) # set turtle speed

t.right(90)  # turn turtle
t.forward(100)  # move and draw
t.left(90)
t.backward(100)

t.goto(100, 100)  # move and draw
t.home()  # move to (0, 0) while drawing

# shorter function names:
t.fd(100)  # forward
t.rt(90)  # right-turn
t.fd(100)
t.rt(90)
t.fd(100)
t.rt(90)
t.fd(100)
# there's also t.lt() for left-turns

# drawing shapes:
t.circle(30)
t.dot(20)  # circle with filling:

# change bg: turtle.bgcolor("blue")
# change title: turtle.title("title")

# to change the look of the turtle: turtle.changesize(i, j, k) (stretch len, stretch width, outline width)
    # this does nothing to the lines drawn 
# change turtle fill color: turtle.fillcolor("red"), and the outline color: turtle.pencolor("green")
# or both at the same time:
turtle.color("red", "green")

# changing pen size:
t.pensize(5)  # meaning changing the line thickness
t.backward(100)


# to fill in a drawing:
t.begin_fill()
## DRAW SHAPE
t.circle(50)
t.end_fill()


# we can change the speed of the turtle with turtle.speed(i), 0<= i <= 10

# doing lots of changes to the pen:
t.pen(pencolor="purple", fillcolor="orange", pensize=10, speed=9)
t.penup()  # picking up the pen, allowing us to move the turtle without draing
t.home()
t.pendown()
t.dot(15)

t.undo()  # undo the previous thing we did
t.clear()  # clear the screen
t.reset()  # resets everything; pen, canvas etc.


# we can stamp with the turtle, leaving an imprint/image of it in place:
stamp_id = t.stamp()
t.fd(50)
# every stamp has an ID, allowing us to remove it later
t.clearstamp(stamp_id)

# we can clone the turtle:
c = t.clone()
c.color("magenta")
t.circle(40)
c.circle(35)



"""
from turtle import *
color('red', 'yellow')
begin_fill()
while True:
    forward(200)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()
done()
"""