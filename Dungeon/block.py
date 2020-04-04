#!/usr/bin/env python3
class block:
    def __init__ (self,char,walkable):
        self.char = char
        self.walkable = walkable
        
    def display(self):
        print(self.char,end="")
        
    def collision(self,other):
        if not self.walkable:
            return None
        
        elif self.walkable:
            return 1
        
    def interaction(self,other):
        pass
        
class tree(block):
    def __init__ (self):
        block.__init__(self,"T",False)
        
class earth(block):
    def __init__ (self):
        block.__init__(self,"e",True)