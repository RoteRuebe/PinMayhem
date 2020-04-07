#!/usr/bin/env python2
import math, copy, pygame, time
pygame.init()

class world:
    def __init__ (self,l):
        self.screen = pygame.display.set_mode((l,l))
        self.l = l
        
    def circle(self,r,M,margin=5):
        for x in range(self.l):
            for y in range(self.l):
                #dis = self.l+1
                dis = 0
                for i in M:
                    rect = pygame.Rect(i,(5,5))
                    self.screen.fill((255,125,125),rect)
                    dis += self.distance([x,y],i)
                    #if dis > self.distance([x,y],i):
                        #dis = self.distance([x,y],i)
                dis /= len(M)    
                
                if abs(dis-r) <= margin:
                    rect = pygame.Rect((x,y),((1,1)))
                    self.screen.fill((255,255,255),rect)
                    
        pygame.display.flip()
        self.screen.fill((0,0,0))
                    
                
                
    
    def distance(self,a,b):
        return math.sqrt( abs(a[0]-b[0])**2 + abs(a[1]-b[1])**2 )
    
class interface:
    def __init__ (self):
        self.M = [(500,500)]
        self.r = 300
        self.w = world(1000)
        
        self.loop()
        
    def loop (self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 13: #enter
                        print("drawing...")
                        self.w.circle(self.r,self.M)
                        print("drawn")
                    
                    elif event.key == 8:  #backspace
                        print("removing point...")
                        min = self.w.l+1
                        point = 0
    
                        for index, i in enumerate(self.M):
                            if self.w.distance(pygame.mouse.get_pos(), i) < min:
                                min = self.w.distance(pygame.mouse.get_pos(), i)
                                point = index
                                
                        print("removed:",self.M[point])
                        self.M.pop(point)
                    
                    elif event.key == 113:  #q
                        self.r = input(":")
                        
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("moving point")
                        min = self.w.l+1
                        point = ()
    
                        for index, i in enumerate(self.M):
                            if self.w.distance(event.pos, i) < min:
                                min = self.w.distance(event.pos, i)
                                point = event.pos,index
                                
                        print("moved:",point)
                                
                        self.M[point[1]] = point[0]
                        
                    elif event.button == 3:
                        print("adding point:",event.pos)
                        self.M.append(event.pos)
interface()
                        