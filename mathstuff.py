from typing import *
# from parseThing import generateShapes
from mathInfo import *


# RECURSIVE_PARTS_2 = [
#     ((0,0),(1/2,0),(1/4,3**0.5/4)),
#     ((1/2,0),(1,0),(3/4,3**0.5/4)),
#     ((1/4,3**0.5/4),(3/4,3**0.5/4),(1/2,3**0.5/2))]

# RECURSIVE_PARTS = []
# for i in RECURSIVE_PARTS_2:
#     RECURSIVE_PARTS.extend([(i[j], i[j+1]) for j in range(len(i)-1)])

# PARTS_TO_SUBDIVIDE = [1]*(len(RECURSIVE_PARTS))

def subdivide(start,end):
    ## Returns a copy of the points in RECURSIVE_PARTS,
    ## but relative to start, end rather than (0,0), (1,0)
    ## start, end are complex numbers, as are all the points returned
    def shift(x,y):
        ## Transformation that shifts (0,0) to start and (1,0) to end
        return (end-start)*complex(x,y) + start
    return [[shift(x,y) for x,y in part] for part in RECURSIVE_PARTS]
    
def recursively_subdivide(start,end,n):
    ## Applies subdivide for n iterations
    parts = subdivide(start,end)
    if n == 1: # one iteration will just call subdivide
        return parts
    # otherwise, go through the subdivided parts to do further subdivision
    new_parts = []
    for part,s in zip(parts,PARTS_TO_SUBDIVIDE):
        # the parts where PARTS_TO_SUBDIVIDE is True will be recursively
        # subdivided further
        if s: 
            new_parts.extend(recursively_subdivide(part[0],part[1],n-1))
        # the parts where PARTS_TO_SUBDIVIDE is False are kept as is
        else:
            new_parts.append(part)
    return new_parts