# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 01:05:41 2025

@author: 1215m
"""

from copy import deepcopy

class Position:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
        
    def __str__(self):
        return f"[{self.q}, {self.r}, {self.s}]"

class Player:
    """
    Variable Explination:
    ============================
    history: Stores a list of positions (Non-inclusive of current pos.) to be used for Trap 3
    position: Current position
    treasure: How many treasure has been picked up
    step: How many steps has been taken
    energy: How many energy has been used
    stepCost: How many steps taken to move to adjacent tile, modify for Reward 1
    energyCost: How many energy is used per step, modify for Reward 2
    
    To Create an create the Pioneer Player: Player([], <Starting Room Position>, 0, 0, 0, <Initial Step Cost>, <Initial Energy Cost>)
    NOTE: When populating Players don't reference the identifiers (i.e p2 = p1) create a deepcopy (i.e p2 = copy.deepcopy(p1))
    """
    
    def __init__(self, history: [Position], position: Position, treasure: int, step: int, energy: int, stepCost: int, energyCost:int):
        self.history = history
        self.position = position
        self.treasure = treasure
        self.step = step
        self.energy = energy
        self.stepCost = stepCost
        self.energyCost = energyCost
    
    #toString method
    def __str__(self):
        num = 1
        posstr = ""
        for pos in self.history:
            posstr += (f"\n{num}." + str(pos))
            num += 1
        return f"History: {posstr}\nCurrent Pos:{self.position}\nSteps:{self.step}, Energy:{self.energy}\nSteps Cost:{self.stepCost}, Energy Cost:{self.energyCost}\nTreasure:{self.treasure}\n"
    
    # Stores the current position in history then sets the position in the parameters to the new one, also adds the steps and energy based on stepCost and energyCost
    def moveTile(self, target: Position):
        #Check weather tile is valid
        self.history.append(self.position)
        self.position = target
        self.step += self.stepCost
        self.energy += self.energyCost
    
    # Testing the functionality of history
    def trap3(self):
        self.position = self.history[-2]
        self.history = self.history[:-2]


#DEBUG DELETE LATER    
"""
p1 = Player([], Position(0, 0, 0), 0, 0, 0, 1, 2)
print(p1)
p1.moveTile(Position(1, -1, 0))
print(p1)
p1.moveTile(Position(1, -2, 1))
print(p1)


p2 = p1 #DO NOT DO THIS
p3 = copy.deepcopy(p1) #DO THIS INSTEAD
p1.moveTile(Position(2, -2, 0))
p3.moveTile(Position(1, -3, 2))
print(p1)
print(p2) #p2 has the same value as p1 (although unaltered) because it references p1
print(p3) #p3 is an entirely new object
"""