from Dictionary import menu
from logo import  coffee_logo
print(coffee_logo)
def money():
	quarters = int(input("How many quarters? "))
	dimes = int(input("How many dimes? "))
	nickels = int(input("How many nickels? "))
	pennies = int(input("How many pennies? "))
	total=quarters*0.25+dimes*0.1+nickels*0.05+pennies*0.01
	return total
def prepare_drink(drink_name, meniu, ingredients):
	recipe = meniu[drink_name]["ingredients"]
	price = meniu[drink_name]["price"]
	totalul=0
	if (ingredients["water_in_machine"] >= recipe["water"] and
			ingredients["milk_in_machine"] >= recipe["milk"] and
			ingredients["coffee_in_machine"] >= recipe["coffee"]):
		budget=money()
		if budget>=price:
			ingredients["coffee_in_machine"]= ingredients["coffee_in_machine"]-recipe["coffee"]
			ingredients["water_in_machine"]=ingredients["water_in_machine"]-recipe["water"]
			ingredients["milk_in_machine"]=ingredients["milk_in_machine"]-recipe["milk"]
			rest = budget - price
			print(f"Here is your rest {round(rest, 1)}$")
			print(f"Here is your {drink_name} ☕")
			totalul=budget-rest
		else:
			print(f"Sorry u don't have enough money {budget} ")
	return totalul
on=input("Type on tu turn on ")
igredients= {
	"milk_in_machine":500,
	"coffee_in_machine":100,
	"water_in_machine":2000
}
incasari=0
coffee_machine=True
while coffee_machine:
	if on=="on":
		print(f"Espresso price:{menu["cafea"]["price"]}", "$")
		print(f"Latte price:{menu["latte"]["price"]}", "$")
		print(f"Cappuccino price:{menu["cappuccino"]["price"]}", "$")
		ask=input("What type of cofee u  want? espresso/latte/cappuccino")
		if ask=="espresso":
			total1=prepare_drink("cafea", menu, igredients)
			incasari += total1
		elif ask=="latte":
			total1=prepare_drink("latte", menu, igredients)
			incasari += total1
		elif ask=="cappuccino":
			total1=prepare_drink("cappuccino", menu, igredients)
			incasari += total1
		elif ask=="report":
			print(igredients)
			print(round(incasari,1))
	off=input("Do u want another drink?")
	if off=="no":
		coffee_machine=False
