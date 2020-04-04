#!/usr/bin/python3

import pickle, token_generator, datetime

class entry:
    def __init__ (self,date,time,till,title,desc=""):
        self.date = date
        self.time = time
        self.till = till
        self.title = title
        self.desc = desc
        
        check_table = {
            self.date:datetime.date,
            self.time:datetime.time,
            self.till:datetime.time,
            self.title:str,
            self.desc:str
        }
        for key, value in check_table.items():
            print( key, value)
            if type(key) != value:
                raise AttributeError("{} is not type, {}".format(key,value))
                
    
    def get(self):
        return {
            "title":self.title,
            "description":self.desc,
            "date":self.date,        
            "time":(self.time,self.till)
        }
    
    def save(self):
        token = token_generator.main()
        with open("./entries/"+token,"wb") as f:
            pickle.dump(self,f)
            

if __name__ == "__main__":
    import sys
    entry(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]).save()