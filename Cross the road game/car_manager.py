from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 3


class CarManager(Turtle):

    current_speed = STARTING_MOVE_DISTANCE

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color(random.choice(COLORS))
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.setheading(180)

        random_y = random.randrange(-240, 240)
        random_x = random.randrange(230, 270)
        self.goto(random_x, random_y)


        self.move_speed = CarManager.current_speed

    def move(self):

        self.fd(self.move_speed)

    def increase_speed(self):

        self.move_speed = CarManager.current_speed

    @classmethod
    def level_up(cls):

        cls.current_speed += MOVE_INCREMENT