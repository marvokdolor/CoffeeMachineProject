from menu import MENU, resources, money
from art import logo


def enough_ingredients(drink: str) -> bool:
    """Takes a drink string and returns a boolean re: whether there are enough ingredients."""
    for item in resources:
        # To handle missing milk key for espresso
        try:
            if MENU[drink]['ingredients'][item] > resources[item]:
                print(f"Sorry, not enough {item}.")
                return False
        except KeyError:
            pass
    return True


def manage_deposits(drink: str) -> str:
    """Takes a drink string and lets the user know if they have sufficient money and if so, calculates and offers up
    their change."""
    drink_cost = MENU[drink]["cost"]
    deposit = 0
    change = 0
    print("Please insert coins.")
    for coin in money:
        number_of_coins = float(input(f"How many {coin}: "))
        deposit += number_of_coins * money[coin]

    if deposit < drink_cost:
        return f"Sorry, that's not enough money. Money refunded."
    else:
        change = deposit - drink_cost
        return f"Here's your drink and ${'{:.2f}'.format(change)} in change."


def manage_ingredients(drink: str) -> dict:
    """Take a drink string and returns an updated 'resources' dictionary, based on ingredients used."""
    for item in resources:
        # To handle missing milk key for espresso
        try:
            resources[item] -= MENU[drink]['ingredients'][item]
        except KeyError:
            pass
    return resources


machine_on = True
profits = 0
print(f"{logo}espresso: $1.50 latte: $2.50 cappuccino: $3.00\n")

while machine_on:

    choice = input(f"What would you like? (espresso/latte/cappuccino): ").lower()

    if choice == "off":
        print("Goodbye.")
        machine_on = False
    elif choice == "report":
        for item in resources:
            print(f"{item.capitalize()}: {resources[item]}")
        print(f"Money: ${'{:.2f}'.format(profits)}")
    elif choice == "espresso" or choice == "latte" or choice == "cappuccino":
        if enough_ingredients(choice):
            print(manage_deposits(choice))
            manage_ingredients(choice)
            # Pocket the cash
            profits += MENU[choice]["cost"]
        else:
            available_drinks = [drink for drink in MENU if enough_ingredients(drink)]
            print(f"""Only {available_drinks} are available.\n(Psst...if that's an empty list, I recommend responding
            with 'off' to the next prompt.)""")
    else:
        print(f"I'm sorry I'm not sure what you mean by: '{choice}.' Let's try that again.")
