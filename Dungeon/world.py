#!/usr/bin/env python3
import block, copy

class world:
    def __init__ (self,size=5):
        self.matrix = []
        self.size = size
        self.entitys = []
        
        row = []
        for _ in range(size):
            row.append(block.earth())
        for _ in range(size):
            self.matrix.append(copy.deepcopy(row))
            
    def collision()
            
    def register_entity(self,new):
        self.entitys.append(new)
            
    def display (self):
        for row in self.matrix:
            for cell in row:
                 cell.display()
            print()
        for entity in self.entitys:
            print(entity.char)
            print(entity.x, entity.y)