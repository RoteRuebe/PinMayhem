#!/usr/bin/python
import time, pygame
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)




class serial():
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

    def hasState(self,index):
        return self.pins[index]
        

array = serial()
while True:
    x = 0
    pygame.display.init()
    screen = pygame.display.set_mode((800,100))
    for cell in array.pins:
        rectangle = pygame.Rect(x,0,100,100)
        if cell:
            screen.fill((100,100,255),rectangle)
        else:
            screen.fill((0,0,0),rectangle)
        x += 100
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            index = pygame.mouse.get_pos()[0]/100
            if array.pins[index]:
                array.on(index)
            else:
                array.off(index)
            
    
    time.sleep(0.3)
            
    
    pygame.display.flip()