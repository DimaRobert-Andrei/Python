import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import random
CAR_GENERATION_CHANCE = 4
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
player = Player()
scoreboard = Scoreboard()
car_list=[]
game_is_on = True
screen.listen()
screen.onkeypress(player.move, "Up")
while game_is_on:
    time.sleep(0.1)
    screen.update()
    if random.randint(1, CAR_GENERATION_CHANCE) == 1:
        new_car = CarManager()
        car_list.append(new_car)
    for car in car_list:
        car.move()
    for car in car_list:
        if car.distance(player) < 10:
            game_is_on = False
            scoreboard.game_over()
    if player.ycor()>280:
        player.reset_position()
        scoreboard.increase_score()
        CarManager.level_up()
        for car in car_list:
            car.increase_speed()


screen.exitonclick()