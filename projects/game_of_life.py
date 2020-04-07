#!/usr/bin/python
import copy, subprocess, random, pygame, time
pygame.display.init()
class cell:
    def __init__ (self,alive=False, history_cap=40):
        self.history_cap = history_cap
        self.IsAlive = alive
        self.counter = 0
        self.history = []
        
    def check(self):
        if self.IsAlive:
            if self.counter in [2,3]:
                pass
            else:
                self.kill()
        else:
            if self.counter == 3:
                self.give_birth()
                
        self.counter = 0
    
    def increment(self):
        self.counter += 1
        
    def give_birth(self):
        self.IsAlive = True
        
    def kill(self):
        self.IsAlive = False
        
    def add_history(self):
        self.history.append(self.IsAlive)
        if len(self.history) > self.history_cap:
            self.history.pop(0)
            
    def set_as_history(self,steps=1):
        try:
            self.IsAlive = self.history[steps*-1]
            self.history.pop(-1)
        except:
            pass
        

    def __str__ (self):
        if self.alive:
            return "[48;5;1m  [0m"
        else:
            return "[48;5;232m  [0m"

        
class world:
    def __init__(self,length,height):
        self.world = []
        self.row = []
        
        for _ in range(length):
            self.row.append(cell())
        
        for _ in range(height):
            self.world.append(copy.deepcopy(self.row))
            
    def generation(self):
        for rindex,row in enumerate(self.world):
            for cindex, cell in enumerate(row):
                if cell.IsAlive:
                    for addr, addc in zip([1,1,1,-1,-1,-1,0,0],[0,1,-1,0,1,-1,1,-1]):
                        try:
                            self.world[rindex+addr][cindex+addc].increment()
                        except:
                            pass
          
        self.add_history()
        for row in self.world:
            for cell in row: 
                cell.check()
                
    def add_history(self):
        for row in self.world:
            for cell in row:
                cell.add_history()
        
    def soup(self):
        for row in self.world:
            for cell in row:
                cell.kill()
        for _ in range(len(self.world)*len(self.row)/3):
            y = int(random.uniform(0,len(self.world)))
            x = int(random.uniform(0,len(self.row)))
            self.world[y][x].give_birth()
        
    def set_as_history(self):
        for row in self.world:
            for cell in row:
                cell.set_as_history()
        

    def __str__ (self):
        fin = ""
        for row in self.world:
            for cell in row:
                fin += str(cell)
            fin += "\n"
        return fin
    
class game():
    def __init__(self,screen=(1800,720),gameworld=(130,72),colorOn=(2,200,200),colorOff=(0,0,0),delay_simulate=0.01,\
    delay_draw=0.01,delete_all=pygame.K_BACKSPACE,end=pygame.K_SPACE,gen_forwards=pygame.K_RIGHT,gen_backwards=pygame.K_LEFT):
        
        pygame.display.init()
        
        self.gameworld = world(gameworld[0],gameworld[1])
        self.screen = pygame.display.set_mode((screen[0],screen[1]))
        self.colorOn = colorOn
        self.colorOff = colorOff
        self.pixel_size = 10
        
        self.delay_simulate = delay_simulate
        self.delay_draw = delay_draw
        self.delete_all = delete_all
        self.end = end
        self.gen_forwards = gen_forwards
        self.gen_backwards = gen_backwards
    
        self.init()
        
    def init(self):
        while True:
            self.mode_draw()
            self.mode_simulate()
        
    def displayit(self):
        corx = -self.pixel_size
        cory = -self.pixel_size
        for row in self.gameworld.world:
            cory += self.pixel_size
            for cell in row:
                corx += self.pixel_size
                rectangle = pygame.Rect((corx,cory),(self.pixel_size,self.pixel_size))
                if cell.IsAlive:
                    self.screen.fill((self.colorOn),rectangle)
                    
                else:
                    self.screen.fill((self.colorOff),rectangle)
            corx = 0
        pygame.display.flip()
    
    def mode_draw(self):
        while True:
            self.displayit()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x = event.pos[0] - 9
                        y = event.pos[1] - 2
                        quantx = int(float(x/10))
                        quanty = int(float(y/10))
                        if self.gameworld.world[quanty][quantx].IsAlive:
                            self.gameworld.world[quanty][quantx].kill()
                        else:
                            self.gameworld.world[quanty][quantx].give_birth()
                        self.gameworld.add_history()
                            
                    elif event.button == 3:
                        self.gameworld.soup()
                        
                if event.type == 2:   #key pressed
                    if event.key == self.end:
                        return
                            
                    if event.key == self.gen_backwards:
                        self.gameworld.set_as_history()
                    
                    else:            
                        if event.key == self.delete_all:
                            for I in self.gameworld.world:
                                for J in I:
                                    J.kill()
                        
                        if event.key == self.gen_forwards:
                        if event.key == self.gen_forwards:
                            self.gameworld.generation()
            time.sleep(self.delay_draw)
    
    def mode_simulate(self):
        while True:
            self.gameworld.generation()
            self.displayit()
            try:
                time.sleep(self.simulate_delay)
            except:
                self.simulate_delay = 0
            
            for event in pygame.event.get():
                if event.type == 2:   #key pressed
                    if event.key == self.end:
                        return
                    
                    if event.key == add_delay:
                        self.simulate_delay += 0.01
                        print self.simulate_delay
                    
                    if event.key == subtract_delay:
                        if self.simulate_delay != 0:
                            self.simulate_delay -= 0.01
                        print self.simulate_delay

game()