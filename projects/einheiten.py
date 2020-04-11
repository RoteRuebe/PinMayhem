#!/usr/bin/python
class einheit:
    tabelle = {
        ("ohm","*","ampere"):"volt",
        ("volt","/","ampere"):"ohm",
        ("volt","/","ohm"):"ampere",
    }
    def __init__ (self,num,einheit,alph):
        self.num = float(num)
        self.einheit = einheit
        self.alph = alph
        
    def get_type(self,obj1,obj2,op):
        obj1 = obj1.einheit
        obj2 = obj2.einheit

        if (obj1,op,obj2) in einheit.tabelle:
            return einheit.tabelle[(obj1,op,obj2)]
        
        elif (obj2,op,obj1) in einheit.tabelle and op == "*":
            return einheit.tabelle[(obj2,op,obj1)]
        
    
    def __mul__(self,obj2):
        rech = self.num*obj2.num
        type = self.get_type(self,obj2,"*")
        if type == None:
            raise TypeError("Error. Can't multiply "+self.einheit+" with "+obj2.einheit)
        
        return eval(type+"("+str(rech)+")")

    def __div__(self,obj2):
        rech = self.num/obj2.num
        type = self.get_type(self,obj2,"/")
        if type == None:
            raise TypeError("Error. Can't divide "+self.einheit+" with "+obj2.einheit)
        
        return eval(type+"("+str(rech)+")")
     
    def __add__(self,obj2):
        if obj2.einheit == self.einheit:
            return eval(self.einheit+"(self.num+obj2.num)")

    def __sub__ (self,obj2):
        if obj2.einheit == self.einheit:
            return eval(self.einheit+"(self.num-obj2.num)")
        
        
    def __str__ (self):
        p = {
            0:"",
            3:"k",
            -3:"m",
            6:"M",
            -6:"u",
            9:"G",
            -9:"n"
        }
        for key, item in p.items():
            a = self.num/10**key
            if (a >= 1 or item == "n") and (a < 1000 or item == "G"):
                return "%.4g" % (a)+item+self.alph

    def __int__ (self):
        return int(self.num)
    
    def __float__ (self):
        return self.num


def parallel(resistors=()):
    if resistors == ():
        return
    fin = 0
    for I in resistors:
        fin += float(1)/float(I)
        
    return ohm(1/fin)


class volt(einheit):
    def __init__ (self,num):
        self.num = float(num)
        self.einheit = "volt"
        self.alph = "V"
        
class ohm(einheit):
    def __init__ (self,num):
        self.num = float(num)
        self.einheit = "ohm"
        self.alph = "Ohm"
        
class ampere(einheit):
    def __init__ (self,num):
        self.num = float(num)
        self.einheit = "ampere"
        self.alph = "A"
        
        
class kilogramm(einheit):
    def __init__ (self,num):
        self.num = float(num)
        self.einheit = "kilogramm"
        self.alph = "kg"
        
class newton(einheit):
    def __init__ (self,num):
        self.num = float(num)
        self.einheit = "newton"
        self.alph = "N"
        
class meter_sekundenquadrat(einheit):
    def __init__ (self,num):
        self.num = float(num)
        self.einheit = "meter_sekundenquadrat"
        self.alph = "m/s^2"
       

