#!/usr/bin/env python3
import random
class block:
    def __init__ (self,char,walkable,world):
        """a block represents one tile on the map."""
        self.world = world
        self.char = char
        self.walkable = walkable
        
    def tick(self):
        """this function gets called every unit of time.
        you may return certain requests.
        
        Replace yourself with another object by returning
        {"replace":<new instance>} 
        """
        
        return {}
    
    def interact(self,who,tool):
        """this function gets called if this object is being interacted with,
        by "who" and with "what" 
        {"append":["all the drops from interaction inside a list"]}
        {"remove":[everything that should be removed]}
        """
        
        return {"error":"interaction not specified"}
        
    def collision(self,other):
        """this function gets called, when an entity is colliding with this object
        a variable "walkable" is defined, so subclasses dont have to overwrite this
        function just to define if one can walk on this block"""
        
        if self.walkable:
            return {"walk":True}
        
        else:
            return {"walk":False}
        
class tree(block):
    name = "tree"
    def __init__ (self,world):
        block.__init__(self, "T",False,world)
        self._choped = False
        
    def interact(self,who,tool):
        if tool.lookup["tree"]: 
            self._choped = True
            return {"append":("log",)*int(random.uniform(1,3))}
        
        return {"error":"unknown interaction"}
            
    def tick(self):
        if self._choped:
            return  {"replace":earth}
        else:
            return {}
        
class earth(block):
    name = "earth"
    def __init__ (self,world):
        block.__init__(self,"e",True,world)
        
    def tick(self):
        r = random.random()
        if r < 0.001/self.world.tickrate:
            return {"replace":grass}
            
        return {}

class grass(block):
    name = "grass"
    def __init__ (self,world):
        block.__init__(self,"g",True,world)
        
        
class workbench(block):
    craft_table = \
    {"placeholder":("log",),
     "yeehaw":("log","log")}
    name = "workbench"
    def __init__ (self,world):
        block.__init__(self,"W",False,world)
        
    def tick(self):
        return {}
        
    def interact(self,who,tool):
        if "craft" in tool.lookup.keys() and tool.lookup["craft"]:
                
            c = self.world.menu( list(workbench.craft_table.keys()) )
            if who.inv_check(workbench.craft_table[c]):
                return {"remove":workbench.craft_table[c],
                        "append":(c,)}
            else:
                return {}
            
            
        else:
            return {}
            