from typing import *
import math
import numpy as np

class Shape:
    '''
    # Class for a Shape
    '''
    def __init__(self, lines=None, shapes=None):
        if lines is None:
            lines = []
        if shapes is None:
            shapes = []
        self.lines:List[str] = lines
        self.shapes:List[Tuple["Shape", str, str]] = shapes
        self.dataTable = dict()
        self.partsToSubdivide = []
        self.start = 0
        self.end = 1
        self.num_rec = 1
    def __setitem__(self, key, val) -> None:
        # create a variable within this shape
        self.dataTable[key] = self._strip(val)
    def __getitem__(self, key) -> str:
        '''
        get the value of a variable form this shape. Errors if it doesn't exist
        '''
        if (key not in self.dataTable): 
            raise ValueError(f"Invalid variable {key} used in shape. Did you mean ${key}?")
        return self.dataTable[key]
    def addLine(self, line:str) -> None:
        '''
        adds a line to this shape
        '''
        self.lines.append(self._strip(line))
    def popLine(self, ind) -> str:
        '''
        removes a line from this shape by index
        '''
        return self.lines.pop(ind)
    def addShape(self, shape:"Shape", inp:str, outpt:str):
        '''
        adds a shape to this shape
        '''
        self.shapes.append([shape, self._strip(inp), self._strip(outpt)])
    def popShape(self, ind) -> str:
        '''
        removes a shape from this shape by index
        '''
        return self.lines.pop(ind)
    def __call__(self) -> List[Tuple[complex, complex]]:
        # generates the line segments for this shape, given the present data, and returns it
        ans = []
        for line in self.lines:
            ans.append(eval(line))
        for _shape, k, v in self.shapes:
            ans.extend(_shape())
            if isinstance(self.partsToSubdivide, list):
                if (_shape.partsToSubdivide == "ALL_TRUE"):
                    self.partsToSubdivide.extend([1]*len(_shape()))
                elif (_shape.partsToSubdivide == "ALL_FALSE"):
                    self.partsToSubdivide.extend([0]*len(_shape()))
                else:
                    self.partsToSubdivide.extend(_shape.partsToSubdivide)
        return ans
    def _strip(self, expr:str) -> str:
        '''
        '''
        for k, v in self.dataTable.items():
            expr = expr.replace(f"${k}", f"({v})")
        return expr
    
