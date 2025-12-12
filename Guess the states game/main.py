import turtle
import pandas as pd
from states import Create
screen = turtle.Screen()
image="blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
data=pd.read_csv('50_states.csv')
x_c=data.x
y_c=data.y
list_x=x_c.to_list()
list_y=y_c.to_list()
state=data.state
state_name=state.to_list()
new_state=[]
state_guess=[]
game_on=True
turtle.tracer(0)
while game_on:
    answer_state = screen.textinput("Guess the state", "What's another state's name?")
    for i in range(len(state_name)):
        if answer_state==state_name[i]:
            state_guess.append(state_name[i])
            create_state=Create()
            new_state.append(create_state)
            for state in new_state:
                state.goto(x_c[i],y_c[i])
                state.write(state_name[i])
                turtle.update()
    if len(state_guess)>=50:
        game_on=False
    if answer_state=="Exit":
        game_on=False



























screen.title("U.S. States Game")
screen.exitonclick()
