import random
import hangmanWords

hangman_stages = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """
]


chosen_word = random.choice(hangmanWords.word_list)
placeholder=["_"]*len(chosen_word)
spatii=""
tries=6
print(chosen_word)
while tries>=0 and "_" in placeholder:
	guess = input("What is tour letter ?")
	if guess in placeholder:
		print("Ati incercat aceasta litera deja ")
	if guess in chosen_word:
		for i in range(len(chosen_word)):
			if chosen_word[i] == guess:
				placeholder[i]=guess
		print("".join(placeholder))

	else:
		tries-=1
		print("Din pacate nu ai ghcit litera")
		if tries == 5:
			print(hangman_stages[0])
		elif tries == 4:
			print(hangman_stages[1])
		elif tries == 3:
			print(hangman_stages[2])
		elif tries == 2:
			print(hangman_stages[3])
		elif tries == 1:
			print(hangman_stages[4])
		elif tries == 0:
			print(hangman_stages[5])

for litera in placeholder:
	spatii+=litera
print(spatii)
if not "_" in spatii:
	print(f"Felicitari ai ghicit cuvantul {spatii}")
else:
	print("Nu ai ghicit cuvantul")
	print("You lose")
	print(hangman_stages[-1])



