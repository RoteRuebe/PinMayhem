# -*- coding: utf-8 -*-
import curses

class select:
    def __init__ (self,choices,box):
        self.l = choices
        self.i = 0
        self.h = "up"
        self.screen = box

    def up(self):
        self.h = "up"
        self.i -= 1
        if self.i < 0:
            self.i = len(self.l)-1
        
    def down(self):
        self.h = "down"
        self.i += 1
        if self.i == len(self.l):
            self.i = 0
            
    def get_selected(self):
        return self.l[self.i]
        
        
    def display(self):
        self.screen.clear()
        for index, element in enumerate(self.l):
            if index == self.i:
                self.screen.addstr(index,0,element,curses.A_REVERSE)
            else:
                self.screen.addstr(index,0,element)
        self.screen.refresh()