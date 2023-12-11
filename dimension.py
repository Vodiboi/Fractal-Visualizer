from typing import *
import numpy as np

def draw_line(mat, x0, y0, x1, y1, inplace=False):
    if not (0 <= x0 < mat.shape[0] and 0 <= x1 < mat.shape[0] and
            0 <= y0 < mat.shape[1] and 0 <= y1 < mat.shape[1]):
        raise ValueError('Invalid coordinates.')
    if not inplace:
        mat = mat.copy()
    if (x0, y0) == (x1, y1):
        mat[x0, y0] = 1
        return mat if not inplace else None
    # Swap axes if Y slope is smaller than X slope
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        mat = mat.T
        x0, y0, x1, y1 = y0, x0, y1, x1
    # Swap line direction to go left-to-right if necessary
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    # Write line ends
    mat[x0, y0] = 1
    mat[x1, y1] = 1
    # Compute intermediate coordinates using line equation
    x = np.arange(x0 + 1, x1)
    y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
    # Write intermediate coordinates
    mat[x, y] = 1
    if not inplace:
        return mat if not transpose else mat.T



INF = int(1e9)
def getDimension(lines:List[Tuple[Tuple[int, int]]], res = 16) -> int:
    if res == 0: return 1
    # grid = [[0]*res for i in range(res)]
    grid = np.zeros((res, res))
    # print(len(lines))
    # probably could do faster with numpy
    maxx = -INF
    maxy = -INF
    minx = INF
    miny = INF
    for i in range(len(lines)):
        for j in lines[i]:
            minx = min(minx, j[0])
            maxx = max(maxx, j[0])
            miny = min(miny, j[1])
            maxy = max(maxy, j[1])
    
    xRangeLen = maxx-minx
    yRangeLen = maxy-miny

    # shift into this list
    f = lambda x: int((x-minx) * (res-1) / xRangeLen) if xRangeLen != 0 else 0
    g = lambda y: int((y-miny) * (res-1) / yRangeLen) if xRangeLen != 0 else 0
    for i in range(len(lines)):

        draw_line(grid, f(lines[i][0][0]), g(lines[i][0][1]), f(lines[i][1][0]), g(lines[i][1][1]), inplace=True)
        # for j in lines[i]:

        #     grid[g(j[1])][f(j[0])] = 1
        #     # print(j[0], f(j[0]))
        #     # print(j[1], g(j[1]))
        # # print()
    # for i in range(len(grid)):
    #     for j in range(len(grid)):
    #         print(grid[i][j], end = "")
    #     print()
    # print(res, sum([sum(i) for i in grid]))
    print(res)
    print(grid)
    return grid.sum()


# print(getDimension([((0, 0), (1, 2)), ((0, 0), (1, 1))], 32) / getDimension([((0, 0), (1, 2)), ((0, 0), (1, 1))], 16))




