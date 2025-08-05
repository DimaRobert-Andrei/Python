def encrypt(message,shift):
	message1=""
	num=""
	simb=""
	for letter in message:
		if letter in alfabet:
			position= alfabet.index(letter)
			position_shifted=(position+shift)%26
			message1 += alfabet[position_shifted]
		elif letter in numbers:
			num+=letter
		elif letter in symbols:
			simb+=letter
	message1+=num+simb
	print(message1)


def decrypt(message,shift):
	message2=""
	num=""
	simb=""
	for letter in message:
		if letter in alfabet:
			position= alfabet.index(letter)
			position_shift=(position-shift)%26
			message2 += alfabet[position_shift]
		elif letter in numbers:
			num += letter
		elif letter in symbols:
			simb += letter
	message2 += num + simb

	print(message2)


alfabet = [
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
	'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '\\', '|', '`', '~']



continuam = "y"
while continuam=="y":
	direction = input("Type encode to encrypt,type decode to decrypt:\n")
	if direction == "encode":
		text = input("Your message is :\n")
		shift_amount = int(input("Type the shift number :\n"))
		encrypt(message=text, shift=shift_amount)
		continuam = input("Continue? [y/n]")


	elif direction == "decode":
		text = input("Your message is :\n")
		shift_amount = int(input("Type the shift number :\n"))
		decrypt(message=text, shift=shift_amount)
		continuam = input("Continue? [y/n]")

