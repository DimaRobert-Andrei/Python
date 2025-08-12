import random
import art
numbers=range(1,101)
incercari=True
def generate_number():
	number_generated=random.choice(numbers)
	return number_generated
number_generate=generate_number()
print(art.logo)
choice = input("Would you like to play easy or hard mode? ")
if choice == "easy":
	incercari = 10
	while incercari>0:

		if choice=="easy":
			incercari=10
			guess=int(input("You have 10 tries.Guess the number between 1 and 100: "))
			if guess<number_generate:
				print(f"You are to low .Remainig tries:{incercari-1}")

			elif guess>number_generate:
				print(f"You are to high .Remainig guess {incercari-1}")

			elif guess == number_generate:
				print("You guessed the number correctly!")
				break
			incercari-=1

elif choice=="hard":
	incercari=5
	while incercari>0:
		guess1 = int(input("You have 5 tries.Guess the number between 1 and 100: "))
		if guess1<number_generate:
			print(f"You are to low .Remainig tries:{incercari-1}")

		elif guess1>number_generate:
			print(f"You are to high .Remainig guess {incercari-1}")

		elif guess1 == number_generate:
			print("You guessed the number correctly!")
			break
		incercari-=1

if incercari==0:
	print(f"You did not guess the number {number_generate}.")