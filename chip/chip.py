#!/usr/bin/python
import time, pygame
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class chip():
    def __init__ (self,pin_input=22,pin_latch=17,pin_clock=27,delay=0):
        self.pin_input = pin_input
        self.pin_latch = pin_latch
        self.pin_clock = pin_clock
        self.delay = delay
        
        self.push("00000000")
        self.pins = [0,0,0,0,0,0,0,0]

        GPIO.setup(self.pin_input,GPIO.OUT)
        GPIO.setup(self.pin_latch,GPIO.OUT)
        GPIO.setup(self.pin_clock,GPIO.OUT)

            
    def cycle(self,input,data=False,delay=0):
    	if input:
    		GPIO.output(self.pin_input,GPIO.HIGH)
    	else:
    		GPIO.output(self.pin_input,GPIO.LOW)
    
    	GPIO.output(self.pin_clock,GPIO.HIGH)
    	if data:
    		GPIO.output(self.pin_latch,GPIO.HIGH)
    	time.sleep(self.delay)
    	GPIO.output(self.pin_latch,GPIO.LOW)
    	GPIO.output(self.pin_clock,GPIO.LOW)
    	time.sleep(self.delay)
    
    
    def push(self,inp,delay=0,doData=False):
    	GPIO.output(self.pin_input,GPIO.LOW)
    	GPIO.output(self.pin_clock,GPIO.LOW)
    	GPIO.output(self.pin_latch,GPIO.LOW)
    
    	if type(inp) == str:
    		fin = []
    		for I in inp:
    			fin.append(int(I))
    		inp = fin
    
    	for index, I in enumerate(inp):
    		if index == len(inp)-1:
    			doData = True
    		if I == 0:
    			self.cycle(False,doData,delay)
    		elif I == 1:
    			self.cycle(True,doData,delay)
    
    	GPIO.output(self.pin_input,GPIO.LOW)
    	GPIO.output(self.pin_latch,GPIO.LOW)
    	GPIO.output(self.pin_clock,GPIO.LOW)

    def on(self,index):
        self.pins[index] = 1
        self.push(self.pins)
        
    def off(self,index):
        self.pins[index] = 0
        self.push(self.pins)

    def blink(self,index,times,t_on=1,t_off=None):
        if t_off == None:
            self.blink(index,t_on,t_on)
            return

        for _ in range(times):
            self.on(index)
            time.sleep(t_on)
            self.off(index)
            time.sleep(t_off)

    def dis_bin(self.num):
        if type(num) == bytearray:
            num = str(bin(int(num)))
        elif type(num) == int:
            num = str(num)
        self.push(num)

    def dis_analog(self,num,LeftToRight=True):
        fin = []
        for _ in range(num):
            fin.append(1)
        for _ in range(8-num):
            fin,append(0)
        if not LeftToRight:
            fin.reverse()
        self.push(fin)


    def getState(self,index):
        return self.pins[index]

