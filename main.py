from menu import MENU, resources, money
from art import logo


def enough_ingredients(drink: str) -> bool:
    """Takes a drink string and returns a boolean re: whether there are enough ingredients."""
    for item in resources:
        # To handle missing milk key for espresso
        try:
            return MENU[drink]['ingredients'][item] <= resources[item]
        except KeyError:
            pass


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
    available_drinks = [drink for drink in MENU if enough_ingredients(drink)]
    # DRINK_CHOICE = input("What would you like? (espresso - $1.50 / latte - $2.50 / cappuccino - $3): ").lower()
    DRINK_CHOICE = input(f"What would you like? ({'/'.join(available_drinks)}): ").lower()

    if DRINK_CHOICE == "off":
        print("Goodbye.")
        machine_on = False
    elif DRINK_CHOICE == "report":
        for item in resources:
            print(f"{item.capitalize()}: {resources[item]}")
        print(f"Money: ${'{:.2f}'.format(profits)}")
    elif DRINK_CHOICE == "espresso" or DRINK_CHOICE == "latte" or DRINK_CHOICE == "cappuccino":
        if enough_ingredients(DRINK_CHOICE):
            print(manage_deposits(DRINK_CHOICE))
            manage_ingredients(DRINK_CHOICE)
            # Pocket the cash
            profits += MENU[DRINK_CHOICE]["cost"]
        else:
            print(f"Sorry, not enough ingredients.")
            available_drinks = [drink for drink in MENU if enough_ingredients(drink)]
            print(f"""Only {available_drinks} are available.\n(Psst...if that's an empty list, I recommend responding 
            with 'off' to the next prompt.)""")
        #TODO specify what is insufficient. Might require a refactor of enough_ingredients.
    else:
        print(f"I'm sorry I'm not sure what you mean by: '{DRINK_CHOICE}.' Let's try that again.")
