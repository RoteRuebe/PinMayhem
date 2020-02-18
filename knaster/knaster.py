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
        lists = self.return_lists(x,y)
        for Iindex,I in enumerate(lists):
            for Jindex,J in enumerate(I):
                try:
                    lists[Iindex][Jindex] = lists[Iindex][Jindex].num
                except:
                    pass
            
        self.exec_combos(x,y,self.check_for_combos_in_list(lists[0]),"row")
        self.exec_combos(x,y,self.check_for_combos_in_list(lists[1]),"column")  
        self.exec_combos(x,y,self.check_for_combos_in_list(lists[2]),"quer1")   
        self.exec_combos(x,y,self.check_for_combos_in_list(lists[3]),"quer2")   

        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
    def return_lists(self,x,y):
        #return lists of row, column and diagonals map(x|y) is part off
        fin_x = []
        fin_y = []
        fin_q1 = []
        fin_q2 = []
        
        fin_y = copy.deepcopy(self.map[y])
        for row in self.map:
            fin_x.append(row[x])
        for index,I in enumerate(fin_x):
            fin_x[index] = I
        for index,I in enumerate(fin_y):
            fin_y[index] = I
            
        if x == y:
            for I in range(5):
                fin_q1.append(self.get(I,I,""))
        else:
            fin_q1 = [None]*5

        if x + y == 4:
            for x,y in ((4,0),(3,1),(2,2),(1,3),(0,4)):
                fin_q2.append(self.get(x,y,""))
        else:
            fin_q2 = [None]*5
            
            
        return fin_x,fin_y,fin_q1,fin_q2
    
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
                    if list.count(J) == 2:
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
        if mode == "row":
            for I in range(num):
                a = None
                for I in self.map[x]:
                    if not I.hasCircle:
                        while True:
                            a,b = self.get_mouse()
                            if a == x:
                                if not self.get(a,b,"circle"):
                                    self.circle(a,b)
                                    pygame.mixer.Sound.play(self.sound_write)
                                    self.display()
                                    break
                                else:
                                    pygame.mixer.Sound.play(self.sound_error)
                            else:
                                pygame.mixer.Sound.play(self.sound_error) 
                        break
                            
        
        if mode == "column":
            for I in range(num):
                a = None
                for I in self.return_lists(x,y)[1]:
                    if not I.hasCircle:
                        while True:
                            a,b = self.get_mouse()
                            if b == y:
                                if not self.get(a,b,"circle"):
                                    self.circle(a,b)
                                    pygame.mixer.Sound.play(self.sound_write)
                                    self.display()
                                    break
                                else:
                                    pygame.mixer.Sound.play(self.sound_error)
                            else:
                                pygame.mixer.Sound.play(self.sound_error)
                        break               
        if mode == "quer1":
            for I in range(num):
                    a = None
                    for I in self.return_lists(x,y)[2]:
                        if not I.hasCircle:
                            while True:
                                a,b = self.get_mouse()
                                if a == b:
                                    if not self.get(a,b,"circle"):
                                        self.circle(a,b)
                                        pygame.mixer.Sound.play(self.sound_write)
                                        self.display()
                                        break
                                    else:
                                        pygame.mixer.Sound.play(self.sound_error)
                                        
                                else:
                                    pygame.mixer.Sound.play(self.sound_error)
                        break
        if mode == "quer2":
            for I in range(num):
                    a = None
                    for I in self.return_lists(x,y)[3]:
                        if not I.hasCircle:
                            while True:
                                a,b = self.get_mouse()
                                if a + b == 4:
                                    if not self.get(a,b,"circle"):
                                        self.circle(a,b)
                                        pygame.mixer.Sound.play(self.sound_write)
                                        self.display()
                                        break
                                    else:
                                        pygame.mixer.Sound.play(self.sound_error)
                                        
                                else:
                                    pygame.mixer.Sound.play(self.sound_error)
                        break                            
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
