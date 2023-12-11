from typing import *
from Shape import Shape

def generateShapes(file:str) -> Dict[str, Shape]:
    '''
    given a file (string) with the correct format, turns it into a shape list
    '''
    f = file.split("\n")
    # data about the present state of the program
    inShape = 0
    shapeName = ""
    curShape = None
    # the dict of shape name:shape
    # note that shapes do not have a name property or field
    ans = dict()
    for num, line in enumerate(f):
        if line.startswith("struct"):
            # making a new shape
            if inShape:
                # already in a shape, no nesting shapes!
                raise SyntaxError(f"Cannot nest structs! on line {num}")
            # update the state to match this new shape
            inShape = 1
            shapeName = line[line.find(" ")+1:line.find("{")]
            curShape = Shape()
        elif line.startswith("linelist "):
            # making a new shape, but in the format of list of segments and list of subdivisions
            # note that "useshape" does not work in these sorts of shapes
            if inShape:
                # suppose we are in a struct, we cannot next shapes
                raise SyntaxError(f"Cannot nest! on line {num}")
            # add this shape to our list of shapes
            # first: get the info
            shapeName = line[9:line.find(" =")] 
            lst = eval(line[line.find("= ")+1:line.find(";")])
            subdivide = eval(line[line.find(";")+1:len(line)])
            # now, create the shapes using the info.
            curShape = Shape()
            for i in lst:
                curShape.addLine(str(i))
            curShape.partsToSubdivide = subdivide
            ans[shapeName] = curShape
            # this shape was defined on 1 line, so the state is "not in shape" afterwards.
            # these next 3 lines are probably unnececary
            inShape = 0
            shapeName = ""
            curShape = None
        elif inShape:
            # remove trailing and leading space
            line = line.strip()
            # ignore commented parts of the line
            if ("%") in line: line = line[:line.find("%")]
            if line.startswith("}"):
                # break out of current shape
                ans[shapeName] = curShape
                inShape = 0
                shapeName = ""
                curShape = None
            elif line.startswith("let "):
                # define a variable
                var_name = line[4:line.find(" =")]
                var_val = line[line.find("= ")+1:len(line)]
                # print(line, var_name, var_val)
                curShape[var_name] = var_val
                # print(f"|{var_name}|")
            elif line.startswith("line("):
                # generate a line
                curShape.addLine(line[line.find("("):line.rfind(")")+1])
            elif line.startswith("useshape "):
                # use a different shapes' lines as part of this shape
                diff_shapename = line[9:line.find("(")]
                shapes_a = line[line.find("(")+1:line.find(",")]
                shapes_b = line[line.find(",")+1:line.rfind(")")]
                curShape.addShape(ans[diff_shapename], shapes_a, shapes_b)
            elif line.startswith("subdivideList "):
                # updates the list of subdivisions for this shape. 
                # IMPORTANT: former subdivision info is ignored fully
                curShape.partsToSubdivide = eval(line[15:len(line)])
            # DEPRICATED, probably disfunctional: 
            elif line.startswith("START = "):
                curShape.start = eval(line[8:])
            elif line.startswith("END = "):
                curShape.end = eval(line[6:])
            elif line.startswith("NUM_RECURSIONS = "):
                curShape.num_rec = eval(line[17:])
    return ans
