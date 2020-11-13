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
        self.control_entrys = ["--------","<new>","<options>"]
        
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_YELLOW)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        
        self.screen = stdscr
        rectangle(self.screen,0,0,curses.LINES-1,curses.COLS-2)
        self.screen.refresh()


        
        self.body = curses.newwin(self.height,self.width,self.ay,self.ax)
        
        
        self.s_select_data = self.body.subwin(self.height,int(self.width*(2/3)), \
                                           self.ay,int(self.width/3))

        s_selection = curses.newwin(self.height,int(self.width/3-2),self.ay,self.ax)
        self.selector = selector.select([],s_selection)

        self._loadentries()


        
        
        self.data = {"title":"Welcome to this programm","desc":"Tutorial coming soon","info":"","from":"","until":"","importance":1}
        self.mode = "select"
        self.display()

        while True:
            self.loop()
        
        
    def loop(self):
        #manage key input
        t = {
            259:"self.selector.up()",   #up
            258:"self.selector.down()", #down
            10:"self.mode = 'view'",    #enter
            263:"self.mode = 'select'", #backspace
            113:"self.exit()",          #q
            8:"self.delete_entry()" ,   #ctr-backspace
            101:"self.edit_entry()",    #e
            117:"self.open_url()"       #u
        }

        update_display = [10,263]
        try:
            key = self.screen.getch()
            exec(t[key])
            if key in update_display:
                self._refresh_display()
            
        except KeyError:
            pass
        
        except KeyboardInterrupt:
            self.exit()

        #if control entry reached in view mode, skip all controll entries
        if self.mode == "view" and key in (258, 259) and self.selector.get_selected() in self.control_entrys:
            while self.selector.get_selected() in self.control_entrys:
                if self.selector.h == "up":
                    self.selector.up()
                elif self.selector.h == "down":
                    self.selector.down()

        if self.selector.get_selected() in self.control_entrys:
            self.manage_control()

        if self.selector.get_selected() not in self.control_entrys:
            with open(self.selector.get_selected()) as f:
                self.data = eval(f.read())
    
        self.display()            
            
    def display(self):
        if self.mode == "select":
            self._display_select()
            
        elif self.mode == "view":
            self._display_view()

    def manage_control(self):
        if self.selector.get_selected() == "--------":
            if self.selector.h == "down":
                self.selector.down()
            elif self.selector.h == "up":
                self.selector.up()

        if self.selector.get_selected() == "<new>":
            if self.mode == "select":
                self.data = {
                    "title":"create a new entry",
                    "desc":"just hit enter",
                    "info":"","from":"","until":"","importance":""
                }
            elif self.mode == "view":
                create.main(self.body,"create")
                self.mode = "select"
                return

        if self.selector.get_selected() == "<options>":
            self.data = {
                "title":"change settings",
                "desc":"coming soon",
                "info":"","from":"","until":"","importance":""
            }

    def _display_view(self):
        self._display_file(self.body)
        s = "{}/{}".format(self.selector.i+1,len(self.selector.l)-len(self.control_entrys))
        self.body.addstr(0,self.ex-len(s)-3,s)
        self.body.refresh()
        self.body.clear()

    def _display_select(self):
        self.selector.display()
        self._display_file(self.s_select_data)
        self.selector.display()
        self.s_select_data.refresh()
        self.s_select_data.clear()\

    def open_url(self):
        subprocess.run("/mnt/c/Windows/SysWOW64/clip.exe",text=True,input=self.data['url'])
        
    def create_entry (self):
        self._refresh_display()  #this should be in loop function / is done there?
        create.main(self.body,"new")
        self._loadentries()
        self.display()  # this is already done in loop function i think, not gonna delete it though you never know
        
    def edit_entry(self):
        self._refresh_display()  # this too
        create.main(self.body,"edit",self.selector.get_selected(),self.data)
        self._loadentries()
        self.display()
        
    def delete_entry(self):
        subprocess.getoutput("rm "+"'"+self.selector.get_selected()+"'")
        self.loaddata()
        self.display()
        
    def _display_file(self,box):
        box.move(0,0)
        box.addstr(self.data["title"],curses.A_BOLD)
        box.addstr(box.getyx()[0]+2,0,self.data["desc"])
        box.addstr(box.getyx()[0]+1,0,"_____________")
        box.addstr(box.getyx()[0]+2,0,self.data["info"])
        box.addstr(box.getyx()[0]+2,0,"till: "+self.data["until"])
        try:
            if self.daysleft() >= 4:
                effect = 1
            elif self.daysleft() >= 3:
                effect = 2
            else:
                effect = 3
            box.addstr(box.getyx()[0]+2,0,str(self._daysleft())+" days left",curses.color_pair(effect))
        except: pass
    
        t = ["could be ignored","should not be ignored","absolutely fucking important"]
        try: 
            box.addstr(box.getyx()[0]+2,0,t[int(self.data["importance"])-1],curses.color_pair(self.data["importance"]))
        except:
            box.addstr(box.getyx()[0]+2,0,str("importance: "+str(self.data["importance"])))
            
        box.refresh()
        
    def _refresh_display(self):
        self.s_select_data.clear()
        self.body.clear()
        self.s_select_data.refresh()
        self.body.refresh()

    def _loadentries(self):
        out = subprocess.getoutput("ls")
        self.out = out.split("\n")
        if not self.out[0]:
            self.out = []
        self.selector.l = self.out+self.control_entrys
        
    def _daysleft(self):
        until = date(*tuple(map(int,self.data["until"].split(".")))[::-1])
        today = date(*tuple(map(int,time.strftime("%Y/%m/%d").split("/"))))
        return (until-today).days
    
    def exit(self):
        #subprocess.getoutput("cp ./* ../upload")
        self.screen.refresh()
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
