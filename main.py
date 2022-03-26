# -----------------------------------------------------------------------------
# Name:        Avalanche Survival Simulator (main.py)
# Purpose:     Practice dodging avalanches for fun!
#
# Author:      Faizaan A.
# Created:     10-Mar-2022
# Updated:     25-Mar-2022
# -----------------------------------------------------------------------------
import os
import time
import keyboard
import numpy as np

from avasim import AvalancheSim
from avasim import SimState

# NOTE: Main list for progam is in avasim.py!!!

print("\nWELCOME TO AVALANCHE SURVIVAL SIMULATOR!!!")

# Main game function. At the end of every game, user can choose to play again or quit (via recursion)...


def runGame():
    # Ask how many days (int) they'd like to try surviving
    dayCount = 0
    while not dayCount:
        try:
            dayCount = int(
                input("\nEnter how many day(s) you'd like to try surviving? "))
            if dayCount <= 0:
                print("That's not a valid number! Try again.")
                dayCount = 0
        except ValueError:
            print("That's not a valid number! Try again.")
            dayCount = 0

    # Ask user for how many candles they'd like to lit (between 0-3) which determines difficulty of the game
    candleCount = -1
    while not (candleCount > -1 and candleCount < 4):
        try:
            candleCount = int(
                input("\nEnter how many candle(s) you'd like to light (between 0-3)? Less candles mean more avalanches. "))
            if candleCount < 0 or candleCount > 3:
                print("That's not a valid number! Try again.")
                candleCount = -1
        except ValueError:
            print("That's not a valid number! Try again.")
            candleCount = -1

    # Keep launching avalanches at user until they either dodge them all or die
    avasim = AvalancheSim(dayCount, candleCount)
    while avasim.state == SimState.ONGOING:
        avasim.createAvas()

        # Let user select which position they'd like to stand on using WASD keys
        confirmed = False
        userVertical = 3
        userHorizontal = 3
        while not confirmed:
            board = np.full((7, 7), "-", dtype="str")
            if keyboard.is_pressed("S"):
                userVertical += 1 if userVertical < 6 else 0
            elif keyboard.is_pressed("W"):
                userVertical -= 1 if userVertical > 0 else 0
            elif keyboard.is_pressed("A"):
                userHorizontal -= 1 if userHorizontal > 0 else 0
            elif keyboard.is_pressed("D"):
                userHorizontal += 1 if userHorizontal < 6 else 0
            elif keyboard.is_pressed("X"):
                confirmed = True
            board[userVertical, userHorizontal] = "x"
            # NOTE: time.sleep() is needed for program to function properly in order to register delayed key input
            time.sleep(0.07)

            # Clear the screen (runs on both Windows and Linux distros)
            os.system("cls" if os.name == "nt" else "clear")

            # Print out amount of days to keep track of progress
            print(" " * 3 + f"(DAY {dayCount - avasim.days + 1} / {dayCount})")

            # Print out board so user can see where they are
            print("-" * 17)
            for row in board:
                print("| " + " ".join(row) + " |")
            print("-" * 17)

            print(
                "\nSelect where you'd like to stand on using WASD keys; press X to confirm. ", end="")
        os.system("cls" if os.name == "nt" else "clear")

        # After having confirmed user position, launch avalanches at them and show them where they landed
        avasim.surviveAvas(board, userVertical, userHorizontal)
        print(" " * 3 + f"(DAY {dayCount - avasim.days} / {dayCount})")
        print("-" * 17)
        for row in board:
            print("| " + " ".join(row) + " |")
        print("-" * 17)

        # Let the user know how close they were to an avalanche if the game is still on-going
        if avasim.state == SimState.ONGOING:
            print(
                f"\nThe closest you were to an original avalanche was {avasim.calcClosestAva(userVertical, userHorizontal)}m. Press ENTER to continue...")
            keyboard.wait("enter")

    # If no avalanches hit the user
    if avasim.state == SimState.SURVIVED:
        print("\nAyy, you made it! You are now an avalanche surviving pro :D")
    # Else if user was hit by an avalanche
    elif avasim.state == SimState.DEAD:
        print("\nOh no, you were buried by an avalanche!")

        # Ask if user wants to play again; if yes, re-run the runGame() function via recursion
        userResponse = input("Do you want to play again? ").lower()
        if userResponse == "y" or userResponse == "yes":
            runGame()


runGame()
