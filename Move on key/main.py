from turtle import Turtle,Screen
import random
import turtle
tim = Turtle()
screen = Screen()
color_list=[  (188, 10, 68), (114, 177, 209), (193, 78, 22), (213, 163, 101), (192, 163, 20), (227, 56, 131), (34, 104, 162), (15, 23, 63), (38, 185, 114), (192, 38, 123), (208, 138, 175), (22, 30, 163), (20, 180, 207), (229, 224, 10), (230, 168, 197), (128, 188, 163), (44, 129, 78), (11, 47, 29), (60, 14, 28), (144, 216, 202), (61, 23, 11), (133, 217, 229), (232, 67, 37), (172, 21, 13), (112, 92, 206)]
turtle.colormode(255)

def move():
    tim.pendown()
    tim.fd(50)
def left():
    tim.pendown()
    new_heading=tim.heading()+ 10
    tim.setheading(new_heading)
def right():
    tim.pendown()
    new_heading=tim.heading() -10
    tim.setheading(new_heading)
def back():
    tim.pendown()
    tim.back(20)
def clear():
    tim.clear()
    tim.penup()
    tim.home()
def randomcolor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b
def color():
    tim.color(randomcolor())
screen.listen()
screen.onkey(move, "w")
screen.onkey(left, "a")
screen.onkey(right, "d")
screen.onkey(color, "c")
screen.onkey(back, "s")
screen.onkey(clear, "Delete")
screen.exitonclick()