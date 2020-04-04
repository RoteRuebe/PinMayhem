#!/usr/bin/env python3
import world, entity

class main:
    def __init__ (self):
        self.World = world.world()
        self.Player = entity.player(0,0,self.World)
        
        self.loop()
        
    def loop (self):
        while True:
            self.World.display()
            for ent in self.World.entitys:
                ent.tick()
                

m = main()