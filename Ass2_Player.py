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
    
    def __init__(self, history: list[Position], position: Position, treasure: int, step: int, energy: int, stepCost: int, energyCost:int):
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
    
    #Setters and Getters
    def getHistory(self):
        return self.history
    def getPosition(self):
        return self.position
    def getTreasure(self):
        return self.treasure
    def getStep(self):
        return self.step
    def getEnergy(self):
        return self.energy
    def getStepCost(self):
        return self.stepCost
    def getEnergyCost(self):
        return self.energyCost
    
    def setHistory(self, new: list[Position]):
        self.history = new
    def setPosition(self, new: Position):
        self.position = new
    def setTreasure(self, new: int):
        self.treasure = new
    def setStep(self, new: float):
        self.step = new
    def setEnergy(self, new: float):
        self.energy = new
    def setStepCost(self, new: float):
        self.stepCost = new
    def setEnergyCost(self, new: float):
        self.energyCost = new
        
    # Class Methods
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