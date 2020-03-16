#!/usr/bin/env python2
import random, math, time, os, sys

import matplotlib.pyplot as plt
#plt.axis("on")
#plt.axis("on")
with open(os.devnull,"w") as f:
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame, pygame.gfxdraw
    sys.stdout = oldstdout
    
pygame.display.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

def pi(repetition=500000,plot=True,infinite=False,PlotEvery=1,PrintEvery=1,visualise=True,colorin=(255,0,0),colorout=(0,0,255),doHistory=True,history_max=10000,box_length=5,delay=0.000001):
    plt.yscale("log")
    os.system('setterm -cursor off')
    if visualise:    
        screen = pygame.display.set_mode((500,500))
        pygame.gfxdraw.circle(screen,250,250,250,(255,255,255))
        pygame.gfxdraw.rectangle(screen,pygame.Rect((0,0),(500,500)),(255,255,255))
        pygame.display.flip()
    
    points = {
        0:0,     #square
        1:0      #circle
    }
    
    if visualise:
        color = None
    if doHistory and visualise:
        history = []

    counter = 0
        
    while True:
        try:
            x = random.uniform(-1,1)
            y = random.uniform(-1,1)
            
            if math.sqrt(x**2+y**2) <= 1:
                points[1] += 1
                if visualise:
                    color = colorin       
                
            elif visualise:
                color = colorout
            points[0] += 1
            
            x += 1
            y += 1
            x *= 250
            y *= 250
            x -= 2
            y -= 2
            x = int(x)
            y = int(y)
            
            if doHistory and visualise:
                history.append((x,y))
                if len(history) >= history_max:
                    area = pygame.Rect(history[0],(box_length,box_length))
                    history.pop(0) 
                    screen.fill((0,0,0),area)
                    pygame.display.update(area)
            
            if visualise:
                pygame.gfxdraw.rectangle(screen,pygame.Rect((x-box_length/2,y-box_length/2),(box_length,box_length)),color)
                pygame.display.update(pygame.Rect((x-box_length/2,y-box_length/2),(box_length,box_length)))
                        
            approx = 4/(float(points[0])/points[1])
            diff = approx - math.pi
            
            if plot and counter % PlotEvery == 0:
                plt.scatter(counter,abs(diff))
                plt.pause(1e-100)
            
            if not infinite:
                if counter >= repetition:
                    break
            
            if counter % PrintEvery == 0:
                print "",approx
                if diff >= 0:
                    print "","%.11f"%(diff)
                else:
                    print "%.11f"%(diff) 
                print "\033[3A"
                
            counter += 1
            time.sleep(delay)
            
        except:
            print "aproximation:",4/(float(points[0])/points[1])
            print "better aporximation:",math.pi
            print "difference:",4/(float(points[0])/points[1]) - math.pi
            os.system('setterm -cursor on')
            break
        
print""*3
pi(infinite=True,visualise=False,delay=0,PlotEvery=1000000,PrintEvery=500000)