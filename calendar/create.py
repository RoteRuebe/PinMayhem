#!/usr/bin/env python3
import curses, subprocess

def maketextbox(screen,h,w,y,x,value=""):
    nw = curses.newwin(h,w,y,x)
    nw.addstr(0,0,value)
    txtbox = curses.textpad.Textbox(nw)
    screen.refresh()
    return txtbox

def main(box, mode, filename="", data={}):
    curses.curs_set(True)
    box.clear()
    
    box.addstr(0,0,"file name:")
    box.addstr(1,0,"title:")
    box.addstr(2,0,"desc:")
    box.addstr(3,0,"info:")
    box.addstr(4,0,"from:")
    box.addstr(5,0,"until:")
    box.addstr(6,0,"importance:")
    
    box.refresh()
    
    s = ""
    s = s+filename+"\n"
    
    if mode == "edit":
        for item in data.values():
            if item:
                s += str(item)+"\n"
            else:
                s += "-"+"\n"
    s = s[:-1]
    
    txt = maketextbox(box,7,50,2,15,s)
    
    try:
        txt.edit(terminate)
    except:
        exit()
    
    message = txt.gather().split("\n")

    for i,m in enumerate(message):
        message[i] = m.strip()
        
    w = ["title","desc","info","from","until","importance"]
    d = {}
    for i,j in zip(w,message[1:]):
        if j not in ["-","/","_"]:
            d[i] = j
        else:
            d[i] = ""
            
    try:    d["importance"] = int(d["importance"])
    except: pass

    if mode == "edit":
        subprocess.getoutput("rm "+"'"+filename+"'")
        
    if message[0]:
        with open(message[0],"wt") as f:
            f.write(str(d).replace("\'","\""))
            f.write("\n")
            
    exit() 
    
def exit():
    curses.curs_set(False)
    return
    
def terminate(x):
    if x == 10 and curses.getsyx()[0] == 8: #backspace or enter
        return 7
    else:
        return x
    