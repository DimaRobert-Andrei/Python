from turtle import Turtle
class Score(Turtle):
    def __init__(self,position):
        super().__init__()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.score=0
        self.goto(position)
        self.write(f"Score: {self.score}", align="center", font=("Arial", 18, "normal"))

    def increase_score(self):
        self.score += 1
        self.clear()
        self.write(f"Score: {self.score}", align="center", font=("Arial", 18, "normal"))