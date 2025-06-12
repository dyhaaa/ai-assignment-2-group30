# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 01:05:41 2025

@author: 1215m
"""

class Position:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
        
    def __str__(self):
        return f"[{self.q}, {self.r}, {self.s}]"

class Player:
    
    def __init__(self, history: [Position], position: Position, treasure: int, step: int, energy: int, stepCost: int, energyCost:int):
        self.history = history
        self.position = position
        self.treasure = treasure
        self.step = step
        self.energy = energy
        self.stepCost = stepCost
        self.energyCost = energyCost
    
    def __str__(self):
        num = 1
        posstr = ""
        for pos in self.history:
            posstr += (f"\n{num}." + str(pos))
            num += 1
        return f"History: {posstr}\nCurrent Pos:{self.position}\nSteps:{self.step}, Energy:{self.energy}\nSteps Cost:{self.stepCost}, Energy Cost:{self.energyCost}\nTreasure:{self.treasure}\n"
        
    def moveTile(self, target: Position):
        #Check weather tile is valid
        self.history.append(self.position)
        self.position = target
        self.step += self.stepCost
        self.energy += self.energyCost
        
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
p1.moveTile(Position(2, -2, 0))
print(p1)
p1.trap3()
print(p1)
"""