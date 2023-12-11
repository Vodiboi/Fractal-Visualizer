height = 0.37744
width = 2 * height


## Generalize Koch Snowflake to arbitrary width / height
RECURSIVE_POINTS=[(0,0),((1-width)/2,0),(1/2,height),((1+width)/2,0),(1,0)]
PARTS_TO_SUBDIVIDE = [True,True,True,True]