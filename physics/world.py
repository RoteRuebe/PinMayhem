#!/usr/bin/env python3

class world:
    def __init__(self,gravity,size,surface):
        self.gravity = gravity
        self.size = size
        self.surface = surface
        self.entitys = []
        
    def tick(self):
        for entity in self.entitys:
            entity.tick()
            
    def draw(self,delete=True):
        if delete:  self.surface.fill((0,0,0))
        for entity in self.entitys:
            entity.draw()
            
    def collide(self,you,l,x,y=None):
        if y == None:
            y = x[1]
            x = x[0]
            
        colliding = []
            
        if y < 0:
            colliding.append(0)
        if x + l > self.size:
            colliding.append(1)
        if y + l > self.size:
            colliding.append(2)
        if x < 0:
            colliding.append(3)
            
        for entity in self.entitys:
            if x < entity.x and entity.x < x + l:
                if y < entity.y and entity.y < y+l:
                    colliding.append(entity)
                
            if x < entity.x + entity.l and entity.x + entity.l < x + l:
                if y < entity.y + entity.l and entity.y + entity.l < y+l:
                    colliding.append(entity)
                    
        try:
            colliding.remove(you)
        except:
            pass
        return colliding
        
    def register(self,other):
        self.entitys.append(other)
        self.draw()
        
