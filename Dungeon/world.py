#!/usr/bin/env python3
import block, random, selector, curses
import curses.textpad

class world():
    def __init__ (self,screen,width,length,tickrate):
        """a world is a container of blocks and entitys, in one isolated space"""
        self._matrix = []
        
        curses.textpad.rectangle(screen,0,0,curses.LINES-1,curses.COLS-2)
        self._game_screen = curses.newwin(20,20,1,2)
        
        screen.refresh()
        
        self._selector = selector.select([],curses.newwin(20,20,1,24))
        self.tickrate = tickrate
        self.width = width
        self.length = length
        
        self.key_press = None
        self.entitys = []
        
        row = []
        for _ in range(length):
            for _ in range(width):
                r = random.random()
                if r >= 0.1:
                    row.append(block.earth(self))
                else:
                    row.append(block.tree(self))
     
            self._matrix.append(row)
            row = []    
            
    def tick(self):
        """function to cause an in game tick: after any key press,
        every block or entity object's tick function will get called"""
        
        for ent in self.entitys:
            ent.tick()
            
        x,y = 0,0
        for _ in self._matrix:
            for b in _:
                resp = b.tick()
                if "replace" in resp.keys():
                    self.replace(x,y,resp["replace"](self))
                x += 1
            x = 0
            y += 1
            
    def collide_at(self,x,y,you):
        """instance "you" wants to go to x|y. can it? everyone at that position
        is politely asked their answer parsed and forwarded returned """
        if x < 0 or y < 0 or x == self.width or y == self.length:
            return {"walk":False}
        
        for i in self.entitys:
            if i.x == x and i.y == y:
                eresp = i.collision(you)
                break
        else:
            eresp = {"walk":True}
        bresp =  self._matrix[y][x].collision(you)
        
        return {"walk":eresp["walk"] and bresp["walk"]}
    
    def get_block(self,x,y):
        """return block at x|y"""
        return self._matrix[y][x]
    
    def get_ent_at(self,x,y):
        """return entityes at x|y"""
        f = []
        for e in self.entitys:
            if e.x == x and e.y == y:
                f.append(e)
                
        return f
    
    def get_ent(self,name):
        """get all entitys of a certain kind"""
        f = []
        for e in self.entitys:
            if e.name == name:
                f.append(e)
                
        return f
    
    def replace(self,x,y,new_instance):
        """replace block at x|y with new instance of block"""
        self._matrix[y].pop(x)
        self._matrix[y].insert(x,new_instance)
        
    def register(self,new):
        """every freshly spawned entity has to call this function"""
        self.entitys.append(new)
        
    def deregister(self,you):
        """if an entity seizes to exist, it calls this funtion"""
        self.entitys.remove(you)
        del you
        
    def display (self):
        """function to display the world accordingly"""
        self._game_screen.clear()
        #world
        x,y = 0,0
        for row in self._matrix:
            for cell in row:
                self._game_screen.addstr(y,x,cell.char)
                x += 1
            x = 0
            y += 1
                
        for entity in self.entitys:
            self._game_screen.addstr(entity.y,entity.x,entity.char)
            if entity.name == "player":
                # inv
                x,y = 0,11
                c = set()
                for i in entity.inventory:
                    if i not in c:
                        self._game_screen.addstr(y,x,str(entity.inventory.count(i))+"x"+i)
                        c.add(i)
                    y += 1
            
        #health
        self._game_screen.refresh()
    
    def menu(self,what):
        """build a selection screen with list "what", return selected element """
        self._selector.l = what
        self._selector.display()
        key = None
        while key != 10:
            key = self._game_screen.getch()
            if chr(key) == "w":
                self._selector.up()
            elif chr(key) == "s":
                self._selector.down()
            
            self._selector.display()
            
        self._selector.screen.clear()
        self._selector.screen.refresh()
        return self._selector.get_selected()
    
