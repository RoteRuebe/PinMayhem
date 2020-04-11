#!/usr/bin/python3
import os, subprocess, selector, time, curses, create, sys
from datetime import date
from curses.textpad import rectangle

class main:
    def __init__ (self,stdscr):
        curses.curs_set(False)
        os.chdir("./entries")
        self.ax = 2
        self.ay = 2
        self.ex = curses.COLS-2
        self.ey = curses.LINES-3
        self.width = self.ex - self.ax
        self.height = self.ey -self.ay
        s_selection = curses.newwin(self.height,int(self.width/3),self.ay,self.ax)
        self.selector = selector.select([],s_selection)
        self.control_entrys = ["--------","<new>"]
        
        self.loaddata()
        
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_YELLOW)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        
        self.screen = stdscr
        rectangle(self.screen,0,0,curses.LINES-1,curses.COLS-2)


        
        self.body = curses.newwin(self.height,self.width,self.ay,self.ax)
        
        
        self.s_select_data = self.body.subwin(self.height,int(self.width*(2/3)), \
                                           self.ay,int(self.width/3))

        
        
        self.data = None
        self.mode = "select"
        self.screen.refresh()
        
        while True:
            self.loop()
        
        
    def loop(self):
        self.show()
        t = {
            259:"self.selector.up()",   #up
            258:"self.selector.down()", #down
            10:"self.mode = 'view'",    #enter
            263:"self.mode = 'select'", #backspace
            113:"self.exit()",          #q
            8:"self.delete()" ,         #ctr-backspace
            101:"self.edit()"           #e
        }
        try:
            key = self.screen.getch()
            exec(t[key])
            
        except KeyError:
            pass
        
        except KeyboardInterrupt:
            self.exit()
            
        if key in [259,258]:
            while self.mode == "view" and self.selector.get_selected() in self.control_entrys:
                if self.selector.h == "up":
                    self.selector.up()
                elif self.selector.h == "down":
                    self.selector.down()
            
    def show(self):
        if self.selector.get_selected() in self.control_entrys:
            self.control()
            
        else:
            with open(self.selector.get_selected()) as f:
                self.data = eval(f.read())
                                    
        if self.mode == "select":
            self.show_select()
            
        elif self.mode == "view":
            self.show_view()
        
    def show_view(self):
        self.clear()
        self.file_info(self.body)
        s = "{}/{}".format(self.selector.i+1,len(self.selector.l)-len(self.control_entrys))
        self.body.addstr(0,self.ex-len(s)-3,s)
        self.body.refresh()

    def show_select(self):
        self.clear()
        self.selector.display()
        self.file_info(self.s_select_data)
        
        self.s_select_data.refresh()
        
        
    def control(self):
        if self.selector.get_selected() == "<new>":
            if self.mode == "select":
                self.data = {
                    "title":"create a new entry",
                    "desc":"just hit enter",
                    "info":"","from":"","until":"","importance":""
                }
                self.show_select()
                
            elif self.mode == "view":
                self.new()
                self.mode = "select"
                
        elif self.selector.get_selected() == "--------":
            if self.selector.h == "down":
                self.selector.down()
            elif self.selector.h == "up":
                self.selector.up()
                
            self.show()
                
    def new (self):
        self.clear()
        create.main(self.body,"new")
        self.loaddata()
        self.show()
        
    def edit(self):
        self.clear()
        create.main(self.body,"edit",self.selector.get_selected(),self.data)
        self.loaddata()
        self.show()
        
    def delete(self):
        subprocess.getoutput("rm "+"'"+self.selector.get_selected()+"'")
        self.loaddata()
        self.show()
        
    def file_info(self,box):
        box.move(0,0)
        box.addstr(self.data["title"],curses.A_BOLD)
        box.addstr(box.getyx()[0]+2,0,self.data["desc"])
        box.addstr(box.getyx()[0]+1,0,"_____________")
        box.addstr(box.getyx()[0]+2,0,self.data["info"])
        box.addstr(box.getyx()[0]+2,0,"from: "+self.data["from"])
        box.addstr(box.getyx()[0]+2,0,"till: "+self.data["until"])
        try:
            if self.daysleft() >= 4:
                effect = 1
            elif self.daysleft() >= 3:
                effect = 2
            else:
                effect = 3           
            box.addstr(box.getyx()[0]+2,0,str(self.daysleft())+" days left",curses.color_pair(effect))
        except: pass
    
        t = ["could be ignored","should not be ignored","absolutely fucking important"]
        try: 
            box.addstr(box.getyx()[0]+2,0,t[int(self.data["importance"])-1],curses.color_pair(self.data["importance"]))
        except:
            box.addstr(box.getyx()[0]+2,0,str("importance: "+str(self.data["importance"])))
            
        box.refresh()
        
    def clear(self):
        self.s_select_data.clear()
        self.body.clear()
        self.s_select_data.refresh()
        self.body.refresh()
        
    def loaddata(self,):
        out = subprocess.run("ls",capture_output=True).stdout
        out = out.decode("utf-8").split("\n")[:-1]
        self.out = out
        self.selector.l = self.out+self.control_entrys
        
    def daysleft(self):
        until = date(*tuple(map(int,self.data["until"].split(".")))[::-1])
        today = date(*tuple(map(int,time.strftime("%Y/%m/%d").split("/"))))
        return (until-today).days
    
    def exit(self):
        self.clear()
        x = 68
        y = 12
        m = curses.newwin(10,71,int(self.height/2-y/2),int(self.width/2-x/2))
        m.addstr(subprocess.getoutput("toilet -f mono12 goodbye"),curses.A_REVERSE)
        m.refresh()
        time.sleep(1)
        sys.exit()

if len(sys.argv) == 2 and sys.argv[1] == "--help":
    s = \
"""
press enter to change to view mode and backspace to return to select mode

when hovering over an entry press e, to make changes to it
in edit mode, press ctrl+c to abort or ctr+d to save changes

create a new entry by selecting <new> (the shortcuts are the same to change mode)
abort the programm with ctr-c or q!
"""
    print(s) 
else:
    curses.wrapper(main)