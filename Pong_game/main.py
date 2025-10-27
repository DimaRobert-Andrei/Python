import time
from turtle import Screen,Turtle
from paddle import Paddle
from ball import Ball
from score import Score
line=Turtle()
line.hideturtle()
screen = Screen()
screen.setup(width=800, height=600)
screen.tracer(0)
line.color("white")
line.penup()
line.goto(0, -300)
first_player = Paddle((-350, 0))
second_player = Paddle((350, 0))
ball = Ball()
score1 = Score((340,270))
score2 = Score((-340,270))
screen.listen()
screen.onkeypress(first_player.up, "w")
screen.onkeypress(first_player.down, "s")
screen.onkeypress(second_player.up, "Up")
screen.onkeypress(second_player.down, "Down")
screen.bgcolor("black")
game_on = True

for _ in range(15):
    line.pendown()
    line.setheading(90)
    line.fd(20)
    line.penup()
    line.fd(20)
    line.pendown()
while game_on:
    screen.update()
    time.sleep(ball.number)
    ball.move()
    if ball.ycor()>280 or ball.ycor()<-280:
        ball.colision()
    if ball.distance(second_player)<50 and ball.xcor()>330 or ball.distance(first_player)<50 and ball.xcor()<-330:
        ball.bounce()
        ball.speed_ball()
    if ball.xcor()<-380:
        score1.increase_score()
        ball.return_ball()
    if ball.xcor()>380:
        score2.increase_score()
        ball.return_ball()




















screen.exitonclick()
