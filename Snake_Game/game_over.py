from turtle import Turtle
class GameOver(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto( 0,0)
        self.color("white")
    def message_game_over(self):

        self.write("GAME OVER", align="center", font=("normal", 15))
