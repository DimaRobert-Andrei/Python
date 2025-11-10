from turtle import Turtle
class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.hideturtle()
        with open("highscore.txt","r") as file:
            self.highscore = int(file.read())
        self.penup()
        self.goto(0, 270)
        self.score=0
        self.write(f"Score: {self.score}", align="center", font=("Arial", 18, "normal"))
        self.update_score()
        self.file()

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_score()
    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.update_score()
    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score} High score:{self.high_score}", align="center", font=("Arial", 18, "normal"))
    def file(self):
        with open("highscore.txt","w") as file:
            file.write(str(self.high_score))
