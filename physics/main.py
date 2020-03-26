#!/usr/bin/env python3
import object, world, pygame
pygame.display.init()
screen = pygame.display.set_mode((500,500))

w = world.world(0.0005,500,screen)

obj = object.object(250,250,50,1,w)
obj.apply_force((10,5))

while True:
    w.tick()
    w.draw()
    pygame.display.flip()
