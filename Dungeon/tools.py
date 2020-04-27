#!/usr/bin/env python3

class tool:
    def __init__ (self,dp):
        """class for tools, that can be wielded and used by entitys
        this would include stuff like armor
        """
        self.dp = dp
        self.lookup = {}
    
    
class fist(tool):
    def __init__ (self):
        tool.__init__(self,5)
        self.lookup = {
            "tree":False,
            "craft":True,
            "stone":False        
        }
        
class axe(tool):
    def __init__ (self):
        tool.__init__(self,10)
        self.lookup = {
        "tree":True        
        }
        
class item(tool):
    def __init__ (self,block):
        tool.__init__(self,5)
        self.lookup = {
            "tree":False,
            "craft":True,
            "stone":False        
        }
        self.block = block
        