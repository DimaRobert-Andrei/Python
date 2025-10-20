from turtle import Turtle,Screen
import random
tim = Turtle()
tom=Turtle()
tem=Turtle()
rob=Turtle()
cla=Turtle()
screen = Screen()
colors = ["red", "blue", "green", "orange", "purple"]
turtle=[tim, tom, tem, rob, cla]

for index,j in enumerate(turtle):
    j.shape("turtle")
    j.color(colors[index])
    j.penup()
    j.goto(-400,-100+index*50)
def random_pace():
    speed=random.randint(5,20)
    return speed
def move():
        for i in turtle:
            i.forward(random_pace())

def start_race():
    race_on=True
    while race_on:
        move()
        for t in turtle:
            if t.xcor()>450:
                winer_color=t.pencolor()
                print(f"{winer_color} a ajuns la finish prima !")
                return winer_color
    return None

def choose_color():
    bet=screen.textinput("Choose a color","Choose a color")
    return bet

def run_game():
    bet1=choose_color()
    winer=start_race()
    if bet1==winer:
        print("You Win!")
    else:
        print("You Lose!")
screen.listen()
screen.onkey(run_game(),"space")
screen.exitonclick()