#!/usr/bin/env python3
import random, tools, keyboard, copy, block
import numpy as nm

class entity:
    def __init__(self,char,x,y,lp,world):
        """an enitity represents something, that is able to
        move and interact with the world."""
        self.x = x
        self.y = y
        self.world = world
        self.char = char
        self.lp = lp
        world.register(self)
    
    def tick(self):
        """this function gets called every unit of time in the game"""
        pass
    
    def collision(self,other):
        """this gets called, when another entity tries to walk all over you
        default is to NOT let that happen"""
        
        return {"walk":False}
    
    def move(self,x,y):
        """tries to move self to pos x y"""
        resp = self.world.collide_at(x,y,self)
        if resp["walk"]:
            self.x = x
            self.y = y
            
        return resp
    
    def hit(self,ent,tool):
        """function gets called, when youre hit by "ent" with "tool" """
        self.lp -= tool.dp
        if self.lp <= 0:
            self.world.deregister(self)
  
class behaviors:
    """entitys can inherit from this class to behave in certain ways"""
    
    def idle(self):
        """behavior where an entity will walk in a random direction every tick"""
        if random.random() <= 1/self.world.tickrate:
            table = [(1,0),(0,1),(-1,0),(0,-1)]
            c = random.choice(table)
            self.move(self.x+c[0],self.y+c[1])
            
    def follow(self,who):
        """behavior where entity will (when path not obstructed, the path finding 
        is none existent) always go in the direction of another given entity"""
        if random.random() <= 1/self.world.tickrate:
            if self.x < who.x:
                self.move(self.x+1,self.y)
    
            elif self.x > who.x:
                self.move(self.x-1,self.y)
    
            elif self.y < who.y:
                self.move(self.x,self.y+1)
                
            elif self.y > who.y:
                self.move(self.x,self.y-1)
        
class sheep(entity,behaviors):
    name = "sheep"
    def __init__ (self,x,y,world):
        entity.__init__(self,"S",x,y,20,world)
        
    def tick(self):
        behaviors.idle(self)
        
class zombie(entity,behaviors):
    name = "zombie"
    def __init__(self,x,y,world):
        entity.__init__(self,"Z",x,y,20,world)
        
    def tick(self):
        for ent in self.world.entitys:
            if ent.name == "player":
                break
        
        if random.random() >= 0.25:
            if nm.sqrt( abs(self.x-ent.x)**2 + abs(self.y-ent.y)**2) < 5:
                behaviors.follow(self,ent)
            
            else:
                behaviors.idle(self)
        
class player(entity):
    name = "player"
    _build_table = {
        "workbench":("log",)
        }
    def __init__ (self,x,y,world):
        entity.__init__(self,"P",x,y,20,world)
        self.inventory = []
        self.equiped = tools.fist()
        self.last_key = None
        self._mode = "move"
        
    def tick(self):    
        #change mode or act according to it
        t = ["i","b","x","w","a","s","d","q","e"]
        
        key = None
        for i in t:
            if keyboard.is_pressed(i):
                if self.last_key != i:
                    key = i
                    self.last_key = i
                
            elif self.last_key == i:
                self.last_key = None
        
        if key == "i":
            self._mode = "ninteract"
            
        elif key == "b":
            self._mode = "build"
            
        elif key == "x":
            self._mode = "attack"
            

        elif key in ["w","a","s","d"]:
                table = {
                 "w":(0,-1),
                 "s":(0,1),
                 "d":(1,0),       
                 "a":(-1,0)
                }
                x = self.x + table[key][0]
                y = self.y + table[key][1]
                exec("self.{}(x,y)".format(self._mode))
                
                self._mode = "move"
        
        elif key == "q":
            self.ti -= 1
        
        elif key == "e":
            self.ti += 1
        
    def inv_remove(self,what):
        """remove items from inventory.
        what = ["list of items to remove"]
        it returns true on sucess and false on failure
        """
        if self.inv_check(what):
            for item in what:
                self.inventory.remove(item)
            return True
        else:
            return False
                
    def inv_check(self,what):
        """check if <what> is subset of inventory"""
        c = copy.deepcopy(self.inventory)
        for i in what:
            if i in c:
                c.remove(i)
            else:
                return False
            
        return True
            
        
    def build(self,x,y): 
        c = self.world.menu(list(player._build_table.keys()))
        req = player._build_table[c]
        
        if self.inv_remove(req):
            exec("self.world.replace(x,y,block.{}(self.world))".format(c))    
        
    def attack(self,x,y):
        e = self.world.get_ent_at(x,y)
        if e:
            for ent in e:
                ent.hit(self,self.equiped)
                
    def ninteract(self,x,y):
        e = self.world.get_block(x,y)
        self.interact(e,self.equiped)    
        
    def interact(self,other,tool):
        """try to interact with "other" (block instance), using "tool" (tool instance)"""
        resp = other.interact(self,tool)
        if "append" in resp:    
            for i in resp["append"]:  self.inventory.append(i)
            
        if "remove" in resp:    self.inv_remove(resp["remove"])