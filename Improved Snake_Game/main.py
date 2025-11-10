import time
from game_over import GameOver
from scoreboard import  Score
from food import Food
from snake import Snake
from turtle import Screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
number=0
screen.tracer(0)
snake = Snake()
food = Food()
stop_game=GameOver()
scoreboard=Score()
screen.update()
screen.listen()
screen.onkey(snake.right, "d")
screen.onkey(snake.left, "a")
screen.onkey(snake.down, "s")
screen.onkey(snake.up, "w")
game_on=True



while game_on:
    colision = snake.body_colision()
    screen.update()
    time.sleep(0.08)
    snake.move()
    if snake.head.distance(food) < 15:
        food.food_update() 
        scoreboard.increase_score()
        snake.extend_segment()
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        scoreboard.reset_score()
        snake.reset()
        scoreboard.file()
    if colision:
        scoreboard.reset_score()
        snake.reset()
        scoreboard.file()






screen.exitonclick()