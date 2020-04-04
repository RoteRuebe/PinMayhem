#!/usr/bin/env python3
class entity:
    def __init__(self,char,x,y,world):
        self.x = x
        self.y = y
        self.w = world
        self.char = char
        world.register_entity(self)
    
    def tick(self):
        pass
    
    def move(self,x,y):
        self.world.collision(x,y)
        self.x = x
        self.y = y
    
    def display(self):
        print(self.char,end="")
        
        
class player(entity):
    def __init__ (self,x,y,world):
        entity.__init__(self,"P",x,y,world)
        
    def tick(self):
        self.move(input("> ")) 
    
    def move(self, direction):
        table = {
         "up":(0,-1),
         "down":(0,1),
         "right":(1,0),       
         "left":(-1,0)
        }
        x += table[direction][0]
        y += table[direction][1]
        entity.move(self,x,y)