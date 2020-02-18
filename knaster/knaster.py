#!/usr/bin/env python3
import copy,random,pygame,time
#bug: fill row  n with circled numbers fill the  column n
#with a certain combo you will not be able to assign the circles at all
#?self.exec_combos()?
pygame.init()
class game:
    def __init__ (self,players):
        self.players = players
        self.dice = [0,0]
        self.loop()
        
    def loop(self):
        while True:
            self.roll_dice()
            for player in self.players:
                player.turn(self.dice)
                time.sleep(0.3)
        
        
    def roll_dice(self):
        self.dice[0] = int(random.uniform(1,6))
        self.dice[1] = int(random.uniform(1,6))
    
class board:
    def __init__ (self,name=""):
        #initalize a 5*5 2d array with cell object s
        row = []
        self.map = []
        
        for I in range(5):
            row.append(cell())
            
        for I in range(5):
            self.map.append(copy.deepcopy(row))
        
        #set constants init sound
        self.offset  =  50
        self.sound_write = pygame.mixer.Sound("write.wav")
        self.sound_error = pygame.mixer.Sound("error.wav")
        
        self.dice = None
        self.name = name
        
        #initialize screen  
        self.dice_img = []
        for I in range(1,7):
            self.dice_img.append(pygame.transform.scale(pygame.image.load("würfel"+str(I)+".jpg"),(50,50)))
            
        self.screen = pygame.display.set_mode((410,410))
        self.screen_game = self.screen.subsurface(pygame.Rect(80,80,self.offset*5,self.offset*5))
        self.font = pygame.font.SysFont("Comic Sans MS",50)
   
    def main (self,x=None,y=None):
        #main loop
        self.display()
        
        what = None
        #loop until cell succesfully changed its state
        if x == None and y == None:
            while what == None:
                x,y = self.get_mouse()
                what = self.do_num(x,y,sum(self.dice)) 
                if what == None:
                    pygame.mixer.Sound.play(self.sound_error)
                
        pygame.mixer.Sound.play(self.sound_write)
                
        self.display()
        #check for combos and let player choose rings
        if what == "write":
            self.combos(x,y)      
        
    def combos(self,x,y):
        #initalize combo searching and execution
        a = self.get_list("row",y)
        b = self.get_list("column",x)
        if x == y:
            c = self.get_list("quer1")
        else:
            c = [None]*5
        if x + y == 4:
            d = self.get_list("quer2")
        else:
            d = [None]*5

        a = self.check_for_combos_in_list(a)
        b = self.check_for_combos_in_list(b)
        c = self.check_for_combos_in_list(c)
        d = self.check_for_combos_in_list(d)
        
        self.exec_combos(x,y,a,"row")
        self.exec_combos(x,y,b,"column")  
        self.exec_combos(x,y,c,"quer1")   
        self.exec_combos(x,y,d,"quer2")   
        
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
    def get_list(self,which,cor=None,get_int=True):
        fin = []
        if which == "row":
            for cell in self.map[cor]:
                if get_int:
                    fin.append(cell.num)
                else:
                    fin.append(cell)
                    
        elif which == "column":
            for row in self.map:
                if get_int:
                    fin.append(row[cor].num)
                else:
                    fin.append(row[cor])
        
        elif which == "quer1":
            for I in range(5):
                if get_int:
                    fin.append(self.map[I][I].num)
                else:
                    fin.append(self.map[I][I])

        elif which == "quer2":
            for I in range(5):
                if get_int:
                    fin.append(self.map[I][4-I].num)
                else:
                    fin.append(self.map[I][4-I])
        
        return fin
    
    def check_for_combos_in_list(self,list):
        #check for certain combos in list and return, how many circles that is worth
        if None in list:
            return 0
        
        for I in range(2,13):
            if list.count(I) == 5:
                return 3
            if list.count(I) == 4:
                return 2
            if list.count(I) == 3:
                for J in range(2,13):
                    if list.count(J) == 2 and J != I:
                        return 2
                return 1
            
            if list.count(I) == 2:
                print(I)
                for J in range(2,13):
                    if list.count(J) == 2 and J != I:
                        print(J)
                        return 1
            
        list.sort()
        for I in range(4):
            if list[I]+1 != list[I+1]:
                return 0
        return 3
            
    def exec_combos(self,x,y,num,mode):
        #let the player choose, where to put num rings
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        
        while num > 0:
            a,b = self.get_mouse()
            if mode == "row":
                check = b == y
            elif mode == "column":
                check = a == x
            elif mode == "quer1":
                check = a == b
            elif mode == "quer2":
                check = a + b == 4
                
            if check and not self.get(a,b,"circle"):
                num -= 1
                self.circle(a,b)
                pygame.mixer.Sound.play(self.sound_write)
                self.display()
            else:
                pygame.mixer.Sound.play(self.sound_error)
                
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
 
    def display (self):
        #draw to the pygame display
        #reset screen
        self.screen.fill((0,0,0))
        #draw meta-information
        dice1 = self.dice_img[self.dice[0]-1]
        dice2 = self.dice_img[self.dice[1]-1]
        self.screen.blit(dice1,(0,0))
        self.screen.blit(dice2,(50,0))
        name = self.font.render(self.name,True,(255,255,255))
        self.screen.blit(name,(205-name.get_width()/2,0))
        
        
        #draw numbers
        x = 0
        y = 0
        for row in self.map:
            for cell in row:
                if cell.num:
                    self.draw_num(x,y,cell.num,cell.hasCircle)
                x += 1
            x = 0
            y += 1
            
        #draw the horizontal lines
        x = 50
        for I in range(5):
            line = pygame.Rect(x,0,3 ,self.offset*5)
            self.screen_game.fill((128,128,128),line)
            x += self.offset
            
        #draw the vertical lines    
        y = 50
        for I in range(5):
            line = pygame.Rect(0,y,self.offset*5 ,3)
            self.screen_game.fill((128,128,128),line)
            y += self.offset
        
        pygame.display.flip()

        
    def draw_num(self,x,y,num,circle):
        #draw a number at pos(x|y)
        x *= self.offset
        y *= self.offset
        
        if circle:
            textsurface = self.font.render("("+str(num)+")", True, (255, 255, 255))
        else:
            textsurface = self.font.render(str(num), True, (255, 255, 255))
        x += self.offset/2 - textsurface.get_width()/2
        y += self.offset/2 - textsurface.get_height()/2
        self.screen_game.blit(textsurface,(x,y))
        pygame.display.flip()
        
    def get_mouse(self):
        #wait for mouse input and return (x|y) of mouse
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x = event.pos[0]
                        y = event.pos[1]
                        x -= self.screen_game.get_offset()[0]
                        y -= self.screen_game.get_offset()[1]
                        x = int(x/self.offset)
                        y = int(y/self.offset)
                        return x,y
            
    def do_num(self,x,y,num):
        return self.map[y][x].do_num(num)
        
    def circle(self,x,y):
        return self.map[y][x].circle()
    
    def get(self,x,y,mode="num"):
        if mode == "num":
            return self.map[y][x].num
        if mode == "circle":
            return self.map[y][x].hasCircle
        else:
            return self.map[y][x]
    
class cell:
    def __init__ (self):
        self.num = None
        self.hasCircle = False
        
    def do_num(self,num):
        #checks if it has to cirlce/write num and does so
        if self.num == None:    
            self.write(num)
            return "write"
    
        elif not self.hasCircle and num == self.num:    
            self.hasCircle = True
            return "circle"
        
        else:   
            return None
        
    def write (self,num):
        if type(num) == int and 2 <= num <= 12:
            self.num = int(num)
            return "write"
        
        else:   
            return None
        
    def circle(self):
        if self.num:
            self.hasCircle = True
            return "circle"
        
        else:   
            return None
        

class player:
    def __init__ (self,name=""):
        self.name = name
        self.board = board(self.name)
        
    def turn(self,dice):
        
        dice = (1,1)
        self.board.dice = dice
        self.board.main()
            
g = game( [player("yannick")] )
