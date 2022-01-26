# -*- coding:utf-8 -*-
import random

# Dice game
def game1():
    amount = int(input('BOT:Please enter the initial amount：'))
    while amount > 0:
        print("BOT:you have %s pound"%amount)
        guess = input('BOT:big or small or stop:')    # Guess the big, guess the small or stop the game
        if guess != 'big' and guess != 'small' and guess != 'stop':
            print("BOT:your input is wrong, please input again")
            continue
        if guess == 'stop':
            print('BOT:Game over')
            break
        else:
            bet = int(input("BOT:bet:"))
            if bet > amount:
                print("BOT:Your amount is insufficient, please place another bet!")
                continue
            else:
                points = random.randint(1, 6)     # Randomly a number from 1 to 6
                print(points)
                if 0< points <=3 and guess == 'small' or 3 < points <= 6 and guess == 'big':
                    print('BOT:you win!')
                    amount = amount+bet
                elif 0< points <= 3 and guess == 'big' or 3 < points <= 6 and guess == 'small':
                    print('BOT:you lose!')
                    amount = amount-bet
                    if amount == 0:            # The account is 0, the game is over
                        print('BOT:Game over')
                        break
                    else:
                        continue
                    return
