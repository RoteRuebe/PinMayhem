#!/usr/bin/env python3
import object, world, pygame
pygame.display.init()
screen = pygame.display.set_mode((500,500))

w = world.world(0,500,screen)

obj1 = object.physical_object(10,10,50,10,w)
obj1.apply_force((-10,-10))

obj2 = object.physical_object(450,450,50,10,w)
obj2.apply_force((10,10))

while True:
    w.tick()
    w.draw()
    pygame.display.flip()
