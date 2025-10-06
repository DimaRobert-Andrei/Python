from data import question_data
from random import choice
score=0
class Quiz_Game:
    def __init__(self, question, correct_answer):
        self.question = question
        self.correct_answer = correct_answer
continua=True
while continua:
    intrebare = choice(question_data)
    quiz = Quiz_Game(intrebare["text"], intrebare["answer"])
    print(quiz.question)
    answer = input("True or False")
    if intrebare["answer"]==answer:
        score+=1
        print(f"Correct!Your score is {score}")
    else:
        print(f"Incorrect!This was your score {score}")
        continua=False

