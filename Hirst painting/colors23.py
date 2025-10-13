"""import colorgram
rgb_list=[]
colors = colorgram.extract('image2.jpg',30)
for color in colors:
    r=color.rgb.r
    g=color.rgb.g
    b=color.rgb.b
    new_color=(r,g,b)
    rgb_list.append(new_color)
print(rgb_list)"""
import turtle
from turtle import Turtle,Screen
import random
color_list=[ (232, 224, 84), (188, 10, 68), (114, 177, 209), (193, 78, 22), (213, 163, 101), (192, 163, 20), (227, 56, 131), (34, 104, 162), (15, 23, 63), (38, 185, 114), (192, 38, 123), (208, 138, 175), (22, 30, 163), (20, 180, 207), (229, 224, 10), (230, 168, 197), (128, 188, 163), (44, 129, 78), (11, 47, 29), (60, 14, 28), (144, 216, 202), (61, 23, 11), (133, 217, 229), (232, 67, 37), (172, 21, 13), (112, 92, 206)]
tim=Turtle()
tim.hideturtle()
turtle.colormode(255)
tim.pensize(10)
tim.speed("fastest")
tim.setheading(225)
tim.penup()
tim.fd(250)
tim.setheading(360)
def painting():
    for _ in range(9):
        tim.dot(20,random.choice(color_list))
        tim.forward(50)
number=0
for _ in range(10):
    painting()
    number += 50
    x = -176.78
    y = -176.78 + number
    tim.teleport(x, y)







screen= Screen()
screen.exitonclick()