from turtle import Turtle
import random
postion=random.randint(20,70)
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("white")
        self.x_move=10
        self.y_move=10
        self.number=0.1
    def move(self):
        new_x=self.xcor()+self.x_move
        new_y=self.ycor()+self.y_move
        self.goto(new_x,new_y)
    def colision(self):
        self.y_move *=-1

    def bounce(self):
        self.x_move *=-1
    def return_ball(self):
        if self.xcor()>300 or self.xcor()<-300:
            self.goto(0,0)
            self.bounce()
            self.number=0.1
    def speed_ball(self):
        self.number*=0.9

