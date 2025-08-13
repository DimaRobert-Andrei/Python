from Dictionary import instagram_followers
import random

def prima_persoane():
	return random.choice(list(instagram_followers.keys()))
GAME_STARTED=True
def celelalte_persoane():
	altcineva = random.choice(list(instagram_followers.keys()))
	return altcineva
def game(prima_persoana):
	global GAME_STARTED
	print(prima_persoana, instagram_followers[prima_persoana])
	print("VS\n")
	cealalta_persoana=celelalte_persoane()
	print(cealalta_persoana,"?")
	choice=input("\n High or Low ?")
	if choice == "high" and instagram_followers[cealalta_persoana] > instagram_followers[prima_persoana]:
		print("You Got this one !")
		prima_persoana1 = cealalta_persoana
		return prima_persoana1
	elif choice == "low" and instagram_followers[cealalta_persoana] < instagram_followers[prima_persoana]:
		print("You Got this one !")
		prima_persoana1 = cealalta_persoana
		return prima_persoana1
	elif choice== "equal" and instagram_followers[cealalta_persoana] == instagram_followers[prima_persoana]:
		print("You Got this one !")
		prima_persoana1 = cealalta_persoana
		return prima_persoana1
	else:
		print("Sorry u lose ")
		GAME_STARTED=False
		return None
score=0
urmatoarea_persoana=prima_persoane()
while GAME_STARTED:
	urmatoarea_persoana = game(urmatoarea_persoana)
	score+=1
	print(f"Score: {score}")






