#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, pygame, sys, subprocess

class cookies:
    def __init__ (self):
        self.cookies = 0
        self.cookies_per_click = 1
        self.cookies_per_second = 0

    def tick(self,display=True):
        self.cookies += self.cookies_per_second
        if display:
            self.cookies_print()
        
    def click(self,display=True):
        self.cookies += self.cookies_per_click
        if display:
            self.cookies_print()
        
    def cookies_print(self):
        s = '%d' % self.cookies
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
                
        s = s + ','.join(reversed(groups))
        
        print(s)
        print("\033[A",end="")
        

class game:
    def __init__ (self):
        self.clicker = cookies()
        
        pygame.display.init()
        self.screen = pygame.display.set_mode((200,200))
        
        rectangle = ((50,50,100,100))
        self.screen.fill((100,100,100),rectangle)
        
        pygame.display.flip()
        self.loop()
    
    def loop(self):
        c = 0
        while True:  
            c += 1
            self.key_handler()
            if c == 1000:
                c = 0
                self.clicker.tick()
            pygame.time.delay(1)
        
    def buy_menu(self):
        #self.name:(cost,cookies per second)
        self.storefront = {
            "oven":(100,10),
            "cookie farm":(10000,100),
            "cookie monocultur":(50000,5000),
            "cookie factory":(1000000,10000),
            "cookie megafactory":(5000000,50000),
            "cookie nuclear reactor":(100000000,1000000),
            "clicker upgrade":(10,1)
        }
        
        inp = input(":")
        if inp in self.storefront:
            costs = self.storefront[inp][0]
            cps = self.storefront[inp][1]
            if self.clicker.cookies >= costs:
                self.clicker.cookies -= costs
                if inp == "clicker upgrade":
                    self.clicker.cookies_per_click += cps
                else:
                    self.clicker.cookies_per_second += cps
                
        subprocess.call("clear")
        
        
    
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicker.click()
                elif event.button == 3:
                    self.buy_menu()
                
                elif event.button == 2:
                    exec(input("> "))
        
      
Game = game()

