# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 14:55:37 2020

@author: Yannick
"""
import copy, time, pygame, random, sys

class game:
    def __init__ (self,delay=0.05,world_length=50,world_height=50,screen_length=500,\
                  screen_height=500,isPixelSquare=True,growth=1):
        
        pygame.display.init()
        self.screen = pygame.display.set_mode((screen_length,screen_height))
        
        self.game_snake = snakes()
        self.game_world = world(world_height,world_length)
        self.game_fruits = fruits()
        
        self.world_height = world_height
        self.world_length = world_height
        
        self.pixel_length = screen_length/world_length
        self.pixel_height = screen_height/world_height
        
        if isPixelSquare:
            self.pixel_length = min(self.pixel_length,self.pixel_height)
            self.pixel_height = self.pixel_length
        
        self.delay = delay
        self.growth = growth
        
        self.loop()

    def tick(self,doDisplay=True): 
        self.key_handler()
        
        self.fruit_spawner()
        
        self.game_snake.move()
        
        collision = self.game_world.get_obj( self.game_snake.get_head_pos() )
        collision_crd = self.game_snake.get_head_pos()
        self.collision_decision(( collision, collision_crd ))
        
        self.game_world.update( self.game_snake.get_pos(), self.game_fruits.get_pos() )
        
        if doDisplay:
            self.display()
      
    def loop (self):
        while True:
            self.tick()
            time.sleep(self.delay)
            
    def key_handler(self):
        key_table = {
            pygame.K_UP:0,
            pygame.K_RIGHT:1,
            pygame.K_DOWN:2,
            pygame.K_LEFT:3
        }
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.event.clear()
                try:
                    if key_table[event.key]-2 != self.game_snake.dir:
                        self.change_snake_dir(key_table[event.key])  
                except:
                    pass     
    
    def collision_decision(self,collision):
        collision_state = str(collision[0])
        collision_crd = collision[1]
        
        if collision_state == "fruit":
            self.eat_fruit(collision_crd)
            self.grow_snake(self.growth)
            
        if collision_state == "snake":
            self.game_over()
            
        if collision_state == "ground":
            pass
            
        if collision_state not in ["fruit","snake","ground"]:
            self.game_over()
            
    def fruit_spawner(self):
        if self.game_fruits.get_pos() == []:
            ran = random.random()
            if ran >= 0.9:
                self.spawn_fruit((int(random.uniform(0,self.world_length)),int(random.uniform(0,self.world_height))))

        
    def display(self):
        display_table = {
            "ground":(0,0,0),
            "snake":(200,45,75),
            "fruit":(200,200,50)
        }
        
        self.game_world.update(self.game_snake.get_pos(),self.game_fruits.get_pos())
        
        x = 0
        y = 0
        for row in self.game_world.get_array():   
            for cell in row:
                rectangle = pygame.Rect(x,y,self.pixel_length,self.pixel_height)
                self.screen.fill(display_table[str(cell)],rectangle)
                x += self.pixel_length
            x = 0
            y += self.pixel_height
        
        pygame.display.flip()
        
    def game_over(self):
        print ("GAME OVER!")
        print ("Score:"+str((self.get_snake_length()-3)/self.growth))
        sys.exit()
        

        
    def change_snake_dir(self,new_dir):
        self.game_snake.change_dir(new_dir)
        
    def grow_snake(self,growth):
        self.game_snake.add_growth(growth)
        
    def spawn_fruit(self,crd):
        self.game_fruits.spawn(crd)
        
    def eat_fruit(self,crd):
        self.game_fruits.eat(crd)
        
    def get_snake_length(self):
        return len(self.game_snake.snake_ps)

        
class world:
    def __init__ (self,height=10,length=10):
        
        
        
        self.map = []
        row = []
        for I in range(length):
            row.append(pixel("ground"))
            
        for I in range(height):
            self.map.append(copy.deepcopy(row))
            
    def update(self,snake_pos,fruit_pos):
        for row in self.map:
            for cell in row:
                cell.change_state("ground")
        
        for I in snake_pos:        
            self.change_state(I,"snake")
        
        for I in fruit_pos:
            self.change_state(I,"fruit")
            
    def display(self):
        display_table = {
            "ground":"x",
            "snake":"S",
            "fruit":"F",
        }
        
        for row in self.map:
            for cell in row:
                print(display_table[str(cell)],end="")
            
    def change_state(self,crd,new):
        self.map[crd[1]][crd[0]].change_state(new)
        
    def get_obj(self,crd):
        if crd[0] < 0:
            return None
        
        if crd[1] < 0:
            return None
        
        try:    
            return self.map[crd[1]][crd[0]]
        except:
            return None
            print()

    def get_array(self):
        return self.map
            
class pixel:
    def __init__ (self,state="?"):
        self.state = state
    
    def change_state(self,new):
        self.state = new
    
    def __str__(self):
        return self.state     
    
        
class snakes:
    def __init__ (self):
        self.dir = 1
        self.snake_ps = [[1,1],[2,1],[3,1]]  
        
        self.growth_num = 0
                
    def move(self):
        dir_table = {
            0:(0,-1),   
            1:(1,0),
            2:(0,1),
            3:(-1,0)
        }

        new_head = copy.deepcopy(self.snake_ps[-1])
        
        new_head[0] += dir_table[self.dir][0]
        new_head[1] += dir_table[self.dir][1]

        self.snake_ps.append(new_head)
        
        self.growth_handler()
    
    
    def growth_handler(self):
        if self.growth_num > 0:
            self.growth_num -= 1
        else:
            self.snake_ps.pop(0)
       
        
    def add_growth(self,num=1):
        self.growth_num += num
             
    def change_dir(self,new_dir):
        self.dir = new_dir
        
    def get_head_pos (self):
        return self.snake_ps[-1]
        
    def get_pos (self):
        return self.snake_ps
        

class fruits:
    def __init__ (self):
        self.fruit_ps = []
        
    def spawn (self,crd):
        self.fruit_ps.append(crd)
        
    def eat (self,crd):
        crd = tuple(crd)
        if crd in self.fruit_ps:
            self.fruit_ps.remove(crd)
        
    def get_pos (self):
        return self.fruit_ps
        
        


    
g = game(screen_height=750,screen_length=1000,world_height=75,world_length=100,growth=3)
