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
		else:
			print(f"Sorry u don't have enough money {budget} ")
on=input("Type on tu turn on ")
igredients= {
	"milk_in_machine":500,
	"coffee_in_machine":100,
	"water_in_machine":2000
}

if on=="on":
	ask=input("What type of cofee u  want? espresso/latte/cappuccino")
	if ask=="espresso":
		print(menu["cafea"]["price"],"$")
		ask1=input("Dou you want to continue?")
		if ask1=="yes":
			prepare_drink("cafea", menu, igredients)
	elif ask=="latte":
		print(menu["latte"]["price"],"$")
		ask2=input("Dou you want to continue?")
		if ask2=="yes":
			prepare_drink("latte", menu, igredients)
	elif ask=="cappuccino":
		print(menu["cappuccino"]["price"],"$")
		ask3=input("Dou you want to continue?")
		if ask3=="yes":
			prepare_drink("cappuccino", menu, igredients)

