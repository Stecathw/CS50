from cs50 import get_float
from math import trunc


def main():
    # Ask how much is owed
    owed = change_owed()
    # Calculte how many coins are returned
    coins = minimum_number_of_coin(owed)
    print(f"{coins}")
    

def change_owed():
    while True:
        o = get_float("Change owed: ")
        if o > 0:
            break
    return o


def minimum_number_of_coin(x):
    # Convert input to cents
    # Define cents
    cents = x*100
    n = 0
    nquarter = 0
    ndime = 0
    nnickel = 0
    npennie = 0
    # how many quarters ? dimes ? nickels ? pennies ?
    if cents >= 25:
        nquarter = trunc(cents/25)
        n += nquarter
        cents -= nquarter*25
    if cents >= 10:
        ndime = trunc(cents/10)
        n += ndime
        cents -= ndime*10
    if cents >= 5:
        nnickel = trunc(cents/5)
        n += nnickel
        cents -= ndime*5
    if cents >= 1:
        npennie = trunc(cents/1)
        n += npennie
        cents -= npennie*1
    return n        


main()
