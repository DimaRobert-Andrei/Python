from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
menu=Menu()
coffee_maker=CoffeeMaker()
money_machine=MoneyMachine()
name=menu.get_items()
continua=True
while continua:
    order_name = input("What would you like to order? ")

    if order_name=="off":
        continuate=False
    elif order_name=="report":
        coffee_maker.report()
        money_machine.report()

    else:
        drink = menu.find_drink(order_name)r
        if drink:
            if not coffee_maker.is_resource_sufficient(drink):
                print(f"Sorry, not enough ingredients to make {drink.name}. Machine stopping.")
                continua=False
            else:
                if money_machine.make_payment(drink.cost):
                    coffee_maker.make_coffee(drink)
                    print(f"The drink {drink.name} is ready and it cost ${drink.cost}.")
       

