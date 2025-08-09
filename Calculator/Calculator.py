import draw
def add(a,b):
	return a+b
def sub(a,b):
	return a-b
def mul(a,b):
	return a*b
def div(a,b):
	return a/b

def opertii(a,b,operation):
	result=0
	if operation=="*":
		result=mul(a,b)

	elif operation=="/":
		result=div(a,b)

	elif operation=="+":
		result=add(a,b)

	elif operation=="-":
		result=sub(a,b)


	else:
		print("Invalid operation")
	print(draw.calculator_ascii_template.format(result=result))
	return result

a=float(input("What s the first number?"))




should_continue="y"



while should_continue=="y":
	operation = input("Pick an operation:\n""*\n""+\n""-\n""/\n")
	b = float(input("Enter the second number:"))
	a=opertii(a,b,operation)
	should_continue = input("Would you like to continue? (y/n)")









