#!/usr/bin/python
class einheit:
    def __init__ (self,num,einheit,alph):
        self.num = float(num)
        self.einheit = einheit
        self.alph = alph
        
    def tabelle(self,obj1,obj2,op):
        obj1 = obj1.einheit
        obj2 = obj2.einheit
        ##define your einheiten. !use the names you gave the classes!
        tabelle = {
            ("ohm","*","ampere"):"volt",
            ("volt","/","ampere"):"ohm",
            ("volt","/","ohm"):"ampere",
            ("kilogram","*","meter_sekundenquadrat"):"newton",
            ("newton","/","kilogramm"):"meter_sekundenquadrat",
            ("newton","/""meter_sekundenquadrat"):"kilogramm"
        }
        
        if (obj1,op,obj2) in tabelle:
            return tabelle[(obj1,op,obj2)]
        
        elif (obj2,op,obj1) in tabelle and op == "*":
            return tabelle[(obj2,op,obj1)]
        
    
    def __mul__(self,obj2):
        rech = self.num*obj2.num
        ein = self.tabelle(self,obj2,"*")
        if ein == None:
            raise Exception("Error. Can't multiply "+self.einheit+" with "+obj2.einheit)
        
        return eval(ein+"("+str(rech)+")")

    def __div__(self,obj2):
        rech = self.num/obj2.num
        ein = self.tabelle(self,obj2,"/")
        if ein == None:
            raise Exception("Error. Can't divide "+self.einheit+" with "+obj2.einheit)
        
        return eval(ein+"("+str(rech)+")")
     
    def __add__(self,obj2):
        if obj2.einheit == self.einheit:
            return eval(self.einheit+"(self.num+obj2.num)")

    def __sub__ (self,obj2):
        if obj2.einheit == self.einheit:
            return eval(self.einheit+"(self.num-obj2.num)")
        
        
    def __str__ (self):
        p = {
            1:"",
            0.001:"k",
            1000:"m",
            0.000001:"M",
            1000000:"u",
            0.000000001:"G",
            1000000000:"n"
        }
        
        for key,item in p.items():
            if self.num*key <= 999 and self.num*key >= 1:
                vorsatz = item
                number = self.num*key
                break
            try:
                number
            except:
                number = self.num*1000000000
                vorsatz = "n"
            
        return str(number)+" "+vorsatz+self.alph
    
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
       

Uq = volt(5)
Rg = ohm(100000000)
print(Uq)
print(Rg)
print(Uq/Rg)
