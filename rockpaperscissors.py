import random

def rockpaperscissors():
    options = ["rock", 'paper', 'scissors']
    response = input("Do you want to play Rock, Paper, Scissors? (Y/N)")
    while response == "Y" or response == 'y':
        random_number = random.randint(0, 2)
        comp = options[random_number]
        move = input("Choose a Move (rock/paper/scissors):")
        if options.index(move) == random_number + 1 :
            print("CPU played %s. You Win! " %comp)
            response = input("Play again? (Y/N)")
        elif options.index(move) == random_number - 2:
            print("CPU played %s. You Win!" %comp)
            response = input("Play again? (Y/N)")
        elif options.index(move) == random_number:
            print("CPU also played %s. It's a Draw!" %comp)
            response = input("Play again? (Y/N)")
        else:
            print("CPU played %s. You lose! Better luck next time." %comp)
            response = input("Play again? (Y/N)")

rockpaperscissors()