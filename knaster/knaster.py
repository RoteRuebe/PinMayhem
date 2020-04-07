#!/usr/bin/env python3
import copy, random, pygame, time, sys
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
                if player.score == None:
                    player.turn(self.dice)
                    while player.score:
                        player.turn(self.dice)
                    time.sleep(0.3)
                else:
                    for player in self.players:
                        player.get_score()
                    self.game_over()
                    break
                        
    def game_over(self):
        for i in self.players:
            print(i.name,i.score)
            
                    
    def has_combos(self):
        fin = []
        for i in self.players:
            fin.append(i.combos)
                            
    def scores(self):
        fin = []
        for i in self.players:
            fin.append(i.score)
        
        return fin
    
    def roll_dice(self):
        self.dice[0] = int(random.uniform(1,6))
        self.dice[1] = int(random.uniform(1,6))

class board:
    def __init__ (self,name=""):
        #initalize a 5*5 2d array with cell object s
        row = []
        self.written_cells = 0
        self.map = []
        
        self.combos = {}
        
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
   
    def do(self,x,y,display=True):
        if self.written_cells == 25:
            return "everything full"
        
        if not self.combos:
            what = self.do_num(x,y,sum(self.dice))
            if display:
                self.display()
            if what == "write":
                self.written_cells += 1
                out = self.get_combos(x,y)
                for I, sout in zip( (y,x,0,0),out.keys() ):
                    if (sout,I) in self.combos:
                        self.combos[sout,I] += out[sout]
                    elif out[sout] != 0:
                        self.combos[(sout,I)] = out[sout]
                        

        else:
            return self.exec_combo(x,y)
        return what
           
    def game_over(self):
        points = 0
        point_table = {
            ("quer1",0):10,
            ("quer2",0):10,
            ("row",0):9,
            ("row",1):8,
            ("row",2):7,
            ("row",3):6,
            ("row",4):5,
            ("column",0):9,
            ("column",1):8,
            ("column",2):7,
            ("column",3):6,
            ("column",4):5
        }
        for key, value in point_table.items():
            if False in self.get_list(key[0],key[1],"circle"):
                pass
            else:
                points += value
                
        return points
        
    def get_combos(self,x,y):
        #search for combos
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
        
        return {"row":a,"column":b,"quer1":c,"quer2":d}
        
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
    def get_list(self,which,cor=None,get="int"):
        fin = []
        if which == "row":
            for cell in self.map[cor]:
                if get == "int":
                    fin.append(cell.num)
                elif get == "circle":
                    fin.append(cell.hasCircle)
                else:
                    fin.append(cell)
                    
        elif which == "column":
            for row in self.map:
                if get == "int":
                    fin.append(row[cor].num)
                elif get == "circle":
                    fin.append(row[cor].hasCircle)
                else:
                    fin.append(row[cor])
        
        elif which == "quer1":
            for I in range(5):
                if get == "int":
                    fin.append(self.map[I][I].num)
                elif get == "circle":
                    fin.append(self.map[I][I].hasCircle)
                else:
                    fin.append(self.map[I][I])


        elif which == "quer2":
            for I in range(5):
                if get == "int":
                    fin.append(self.map[I][4-I].num)
                elif get == "circle":
                    fin.append(self.map[I][4-I].hasCircle)
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
                for J in range(2,13):
                    if list.count(J) == 2 and J != I:
                        return 1
            
        list.sort()
        for I in range(4):
            if list[I]+1 != list[I+1]:
                return 0
        return 3
            
    def exec_combo(self,x,y):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        for key in self.combos.keys():
            if not self.get(x,y,"circle"):
                if key[0] == "row":
                    if key[1] == y:
                        self.circle(x,y)
                        self.combos[("row",y)] -= 1
                
                elif key[0] == "column":
                    if key[1] == x:
                        self.circle(x,y)
                        self.combos[("column",x)] -= 1
                    
                elif key[0] == "quer1":
                    if x == y:
                        self.circle(x,y)
                        self.combos[("quer1",0)] -= 1
                    
                elif key[0] == "quer2":
                    if x + y == 4:
                        self.circle(x,y)
                        self.combos[("quer2",0)] -= 1
                
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.display()
        self.cleanup_combos()
                        
    def cleanup_combos(self):
        clean = []
        for key, value in self.combos.items():
            if value == 0:
                clean.append(key)
                
            l = self.get_list(key[0],key[1],False)
            for index,I in enumerate(l):
                l[index] = I.hasCircle
                
            if l == [True]*5:
                clean.append(key)
                
        for I in clean:
            self.combos.pop(I)
            
            
    def display (self):
        #draw to the pygame display
        #reset screen
        self.screen.fill((0,0,0))
        #draw meta-information
        border_offset = 15
        dice1 = self.dice_img[self.dice[0]-1]
        dice2 = self.dice_img[self.dice[1]-1]
        self.screen.blit(dice1,(border_offset+dice1.get_width(),410-dice1.get_height()-border_offset))
        self.screen.blit(dice2,(border_offset,410-dice2.get_height()-border_offset))
        name = self.font.render(self.name,True,(255,255,255))
        self.screen.blit(name,(410-name.get_width()-border_offset,410-name.get_height()-border_offset))
        
        x = -self.offset
        y = -self.offset
        for i in 10,9,8,7,6,5:
            cx = self.screen_game.get_offset()[0] + x
            cy = self.screen_game.get_offset()[1] + y
            num = self.font.render(str(i),True,(200,200,200))
            if i != 10:
                self.screen.blit(num,(cx+num.get_width()-2,cy))
            else:
                self.screen.blit(num,(cx,cy))
            x += self.offset
            
        for i in 10,9,8,7,6,5:
            cx = self.screen_game.get_offset()[0] + x
            cy = self.screen_game.get_offset()[1] + y
            num = self.font.render(str(i),True,(200,200,200))
            if i != 10:
                self.screen.blit(num,(cx+num.get_width(),cy+num.get_height()/2-6))
            else:
                self.screen.blit(num,(cx,cy))
            y += self.offset
        
        
        
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
                            if x >= 0 and x < 5 and y >= 0 and y < 5:
                                return x,y
                    
    def in_combos(self,key):
        for I in self.combos:
            if key == I:
                return True
        return False
    
    def get_in_combos(self,key):
        for I in self.combos:
            if key == I:
                return I
        return None
            
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
    def __init__ (self,name):
        self.score = None
        self.name = name
        self.board = board(name)
        
    def turn(self,dice):
        self.board.dice = dice
        self.board.display()
        do = None
        while do == None:
            x,y = self.board.get_mouse()
            do = self.board.do(x,y)
            if do == "everything full":
                self.get_score()
                break   
        
    def get_score(self):
        while self.board.combos:
            self.turn((0,0))
            
        self.score = self.board.game_over()
                
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            

game( list(map(player,sys.argv[1:]))  )
