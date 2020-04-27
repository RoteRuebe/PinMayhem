#!/usr/bin/env python3
import world, entity, curses, time

class main:
    def __init__ (self,screen):
        width = 20
        length = 10
        self.tickrate = 20
        curses.curs_set(False)
        
        self.World = world.world(screen,width,length,self.tickrate)
        
        entity.player(0,0,self.World)
        entity.sheep(5,5,self.World)
        entity.zombie(7,7,self.World)
        a = entity.entity("D",3,3,25,self.World)
        a.name = "d"
        
        self.game_mode()
    
    def game_mode(self):
        while True:
            self.World.tick()
            self.World.display()
            time.sleep(1/self.tickrate)

if __name__ == "__main__":
    curses.wrapper(main)
