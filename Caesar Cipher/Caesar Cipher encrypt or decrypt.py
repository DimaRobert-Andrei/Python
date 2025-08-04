def encrypt(message,shift):
	message1=""
	for letter in message:
		position= alfabet.index(letter)
		position_shifted=(position+shift)%26
		message1 += alfabet[position_shifted]
	print(message1)


def decrypt(message,shift):
	message2=""
	for letter in message:
		position= alfabet.index(letter)
		position_shift=(position-shift)%26
		message2 += alfabet[position_shift]
	print(message2)


alfabet = [
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
	'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
direction=input("Type encode to encrypt,type decode to decrypt:\n")
if direction=="encode":
	text = input("Your message is :\n")
	shift_amount = int(input("Type the shift number :\n"))
	encrypt(message=text, shift=shift_amount)
elif direction == "decode":
	text = input("Your message is :\n")
	shift_amount = int(input("Type the shift number :\n"))
	decrypt(message=text, shift=shift_amount)
else:
	print("Invalid direction")
	quit()

