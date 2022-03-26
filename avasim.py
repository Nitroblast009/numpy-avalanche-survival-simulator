import math
from enum import Enum
import numpy as np


class SimState(Enum):
    # Use Enum class to name values of game state and compare them (either if the user is dead, has survived, or is still playing)
    DEAD = -1
    ONGOING = 0
    SURVIVED = 1


class AvalancheSim:
    def __init__(self, days, candles):
        # Initialize class with specified amount of days to survive and amount of candles lit
        self.days = days
        self.candles = candles

        # Set the temperature (aka difficulty) of the avalanches based on the amount of candles lit
        self.setTemp()

        # Main avalanches list (numpy array) for program!!!
        self.avas = np.zeros((10, 3), dtype="int64")

        self.state = SimState.ONGOING

    def createAvas(self):
        # Give each avalanche array a random x,y value
        for i in range(len(self.avas)):
            for j in range(self.avas.shape[1] - 1):
                self.avas[i, j] = np.random.randint(6)

        # Set each avalanche array's magnitude, based on temperature
        for i in range(len(self.avas)):
            if self.temp <= 0:
                self.avas[i, 2] = np.random.randint(25, 40)
            elif self.temp < 16:
                self.avas[i, 2] = np.random.randint(55, 75)
            elif self.temp < 23:
                self.avas[i, 2] = np.random.randint(75, 90)
            else:
                self.avas[i, 2] = np.random.randint(90, 100)

    def surviveAvas(self, board, userY, userX):
        # See if any avalanches hit user; if so, mark the game as lost
        for ava in self.avas:
            # Calculate chance for avalanche to hit adjacent coordinates, based on magnitude
            chance = ava[2] / 100
            collYs = []
            collXs = []
            if np.random.rand(1)[0] >= chance:
                collYs.append(ava[1] + 1)
            if np.random.rand(1)[0] >= chance:
                collYs.append(ava[1] - 1)
            if np.random.rand(1)[0] >= chance:
                collXs.append(ava[0] + 1)
            if np.random.rand(1)[0] >= chance:
                collXs.append(ava[0] - 1)

            # Mark all spots (including adjacents) hit by avalanche on board
            board[ava[1], ava[0]] = "◙"
            for collY in collYs:
                board[collY, ava[0]] = "◙"
            for collX in collXs:
                board[ava[1], collX] = "◙"

        # Check whether user was hit by avalanche
        if board[userY, userX] == "◙":
            self.state = SimState.DEAD
            return None

        # Go to the next day. If there are no more days, mark the game as won
        self.days -= 1
        if self.days == 0:
            self.state = SimState.SURVIVED

    def setTemp(self):
        # Set temperature of the game based on how many candles are lit; the lower the temperature, the more avalanches will spawn
        if self.candles == 0:
            self.temp = np.random.randint(-20, 1)
        elif self.candles == 1:
            self.temp = np.random.randint(1, 16)
        elif self.candles == 2:
            self.temp = np.random.randint(16, 23)
        else:
            self.temp = np.random.randint(23, 30)

    def calcClosestAva(self, userY, userX):
        avaDistances = []
        # Calculate how for each avalanche was and return closest
        for ava in self.avas:
            # Get x and y difference of each avalanche and use Pythagorean theorem to get resultant distance
            avaY = abs(ava[0] - userY)
            avaX = abs(ava[1] - userX)
            avaDistances.append(math.sqrt(avaY**2 + avaX**2))
        # Return the closest distance (rounded)
        return round(min(avaDistances), 3)
