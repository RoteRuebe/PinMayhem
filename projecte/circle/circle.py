#!/usr/bin/python2
import pygame, random
import pygame.gfxdraw
import numpy as nm

pygame.init()

Font = pygame.font.SysFont("Arial",30)
screen = pygame.display.set_mode((1000,1000))
screen.fill((0,0,0))
pygame.display.flip()

def draw_circle(M,r,surface,color,plot=500):
    rec = pygame.Rect((M[0]-r-1,M[1]-r-1),(2*r+2,2*r+2))
    phi = 0
    lp = M[0],M[1]+r
    for i in range(plot):
        px = int(nm.round(r*nm.sin(phi)+M[0]))
        py = int(nm.round(r*nm.cos(phi)+M[1]))
        pygame.gfxdraw.line(surface,px,py,lp[0],lp[1],color)
        lp = px,py
        phi += 2*nm.pi/plot
    return rec

def circle(M,r,surface,color,lastrec,delete,plot=500,update=True):
    if delete:
        screen.fill((0,0,0),lastrec)
    
    rec = draw_circle(M,r,screen,color)
    
    if update: pygame.display.update(rec)
    if delete and update: pygame.display.update(lastrec)
    return rec

goup = [True]*3
def new_color(old_color):
    new_color = []
    for index,color,up in zip((0,1,2),old_color,goup):
        if color == 254:
            goup[index] = False
        elif color == 1: 
            goup[index] = True
        if up:
            new_color.append(color+1)
        else:
            new_color.append(color-1)
    return new_color

def show_help():
    h = "press tab to change between modes\n\
when in persistent mode:\n\
press any modifier key to draw circles\n\n\
arrow up, arrow down, and scrolling is used to change the radius \n\
press shift+the arrow keys for a smaller change in radius\n\n\
press s to save a color pallet, and g to retrieve one\n\
(it will be picked randomly from your the saved ones)\n"
         
    y = 50
    for i in h.split("\n"):
        a = Font.render(i,True,(255,255,255))
        screen.blit(a,(50,y))
        y += 30
    pygame.display.flip()
    

print('hint: when confused press "h"')
M = [500,500]
r = 200
color = (int(random.uniform(0,255)),int(random.uniform(0,255)),int(random.uniform(0,255)))
delete = True
lastrec = pygame.Rect(0,0,0,0)
while True: 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if pygame.key.get_mods() or delete:
                M = [event.pos[0]+event.rel[0],event.pos[1]+event.rel[1]]
                lastrec = circle(M,r,screen,color,lastrec,delete)
                color = new_color(color)
                    
        elif event.type == pygame.KEYDOWN: 
            if pygame.key.get_mods(): dr = 10
            else: dr = 50
                
            if event.key == pygame.K_UP:
                r += dr
                lastrec = circle(M,r,screen,color,lastrec,delete)
                
            elif event.key == pygame.K_DOWN:
                r -= dr     
                lastrec = circle(M,r,screen,color,lastrec,delete)

            elif event.key == pygame.K_s:
                with open("/home/kinder/git/PinMayhem/projects/circle/colors.txt","at") as f:
                    f.write(str(color)+";"+str(goup)+"\n")
                    
                print("color saved!")
                
            elif event.key == pygame.K_g:
                with open("/home/kinder/git/PinMayhem/projects/circle/colors.txt","rt") as f:
                   txt = random.choice(f.readlines())
                   txt = txt.split(";")
                   color = eval(txt[0]); goup = eval(txt[1])
                print("color chosen!")
                
            elif event.key == pygame.K_h:
                show_help()
                
            elif event.key == pygame.K_TAB:
                delete = not delete
                if delete: screen.fill((0,0,0))
                pygame.display.flip()
                circle(M,r,screen,color,lastrec,delete,update=False)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                r += 1
                
            elif event.button == 5:
                r -= 1
                
            lastrec = circle(M,r,screen,color,lastrec,delete)
