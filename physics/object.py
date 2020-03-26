#!/usr/bin/env python3
import pygame
import pygame.gfxdraw
import numpy as nm

class object:
    def __init__ (self,x,y,m,l,world):
        self.x = x
        self.y = y
        self.l = l
        self.m = m
        self.world = world
        self.world.register(self)
        self.f = [0,0]
        
    def tick(self,gravitate=None,test=False):
        if not test:
            collision = self.world.collide(self.l,self.tick(gravitate,True))
            if collision in [0,2]:
                self.f[1] *= -1
            elif collision in [1,3]:
                self.f[0] *= -1
        
        f = self.gravitate(gravitate,test)
        x = self.x; y = self.y
        
        x += f[0]/self.m
        y += f[1]/self.m
        if not test:
            self.x = x; self.y = y
        return x, y
        
    def gravitate(self,other=None,test=False):
        if other == None:
            return self.accelerate((0,self.world.gravity,test))
        else:
            dx = self.x - other[0]
            dy = self.y - other[1]
            q =  (self.world.gravity**2*dx**2-dy**2)/2
            x = -dy/2 + nm.sqrt((dy/2)**2-q)
            y = x*dy/dx
            return self.accelerate((x,y),test)
        
    def draw(self):
        rect = pygame.Rect(self.x,self.y,self.l,self.l)
        self.world.surface.fill((255,255,255),rect)
        
    def apply_force(self,f,test=False):
        newf=[None]*2
        newf[0] = f[0] + self.f[0]
        newf[1] = f[1] + self.f[1]
        if not test:
            self.f = newf
        return newf
        
    def accelerate(self,v,test=False):
        newf = [None]*2
        newf[0] = v[0] * self.m + self.f[0]
        newf[1] = v[1] * self.m + self.f[1]
        if not test:
            self.f = newf
        return newf