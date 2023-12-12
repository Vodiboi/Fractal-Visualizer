import os
import contextlib

with open(os.devnull, "w") as devnull:
    with contextlib.redirect_stdout(devnull):
        import pygame

import numpy as np

BG_COLOR = 255, 255, 255
LINE_COLOR = 0, 0, 0
BOX_COLOR = 32, 135, 159

def get_mat(a, b, t=False):
    """
    returns the matrix that:
    sends [0, 0, 1] -> a
    sends [1, 0, 1] -> b
    preserves angles
    """
    result = np.array(
        [
            [b[0] - a[0], a[1] - b[1], a[0]],
            [b[1] - a[1], b[0] - a[0], a[1]],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )
    return np.transpose(result) if t else result

def iterate(start, end, segments, parts, iterations):
    if iterations == 0:
        return np.array([[start, end]], dtype=np.float64)

    mats = [get_mat(a, b, True) for a, b in segments]
    result = first_iteration = np.array([[[a, b, 1], [c, d, 1]] for (a, b), (c, d) in segments], dtype=np.float64)

    for _ in range(1, iterations):
        result = np.concatenate([result @ mat if part else [base] for part, mat, base in zip(parts, mats, first_iteration)])

    return (result @ get_mat(start, end, True))[..., :-1]

def scale_segments(segments):
    """
    scale and translate segments to fit inside the unit square.
    returns None, mutates segments.
    """
    segments = np.reshape(segments, (-1, 2))
    segments -= np.min(segments, axis=0)
    segments /= np.max(segments, axis=(0, 1)) + 0.1
    segments += 0.5 - (np.max(segments, axis=0) - np.min(segments, axis=0)) / 2

def get_grid(segments, density):
    """
    returns a density x density array of bools, which is a rendering of segments.
    """
    surface = pygame.Surface((density, density))
    for a, b in np.floor(segments * density).astype(np.int32):
        pygame.draw.line(surface, [255, 0, 0], a, b)
    return pygame.surfarray.array_red(surface) > 1.0

def collapse(grid, factor):
    """
    returns a grid / factor x grid / factor array.
    divides grid into factor x factor squares, and then takes the logical OR of each square.
    """
    slices = np.empty((factor, factor, grid.shape[0] // factor, grid.shape[1] // factor, *grid.shape[2:]))
    for i in range(factor):
        for j in range(factor):
           slices[i, j] = grid[i::factor, j::factor]
    return np.any(slices, axis=(0, 1))

def get_edges(grid):
    result = np.zeros_like(grid, dtype=bool)
    result[:-1, :] |= grid[1:, :]
    result[1:, :] |= grid[:-1, :]
    result[:, :-1] |= grid[:, 1:]
    result[:, 1:] |= grid[:, :-1]
    return np.logical_and(np.logical_not(grid), result)

if __name__ == "__main__":
    from PIL import Image

    from mathInfo import (
        RECURSIVE_PARTS,
        PARTS_TO_SUBDIVIDE,
        START,
        END,
        NUM_RECURSIONS,
        DRAW_BOXES,
    )

    START = START.real, START.imag
    END = END.real, END.imag
    
    if len(RECURSIVE_PARTS):
        segments = iterate(START, END, RECURSIVE_PARTS, PARTS_TO_SUBDIVIDE, NUM_RECURSIONS)
        scale_segments(segments)
        grid = get_grid(segments, 1024)
    else:
        grid = np.zeros((1024, 1024), dtype=bool)

    # grid = get_edges(grid)

    grid_surf = np.full((1024, 1024, 3), BG_COLOR, dtype=np.uint8)

    dimension = np.log2(np.sum(grid, axis=(0, 1)) / np.sum(collapse(grid, 2), axis=(0, 1)))
    print(dimension)

    if DRAW_BOXES is not None:
        box_grid = grid
        for _ in range(DRAW_BOXES):
            box_grid = collapse(box_grid, 2)

        print(int(np.sum(box_grid, axis=(0, 1))))

        for _ in range(DRAW_BOXES):
            box_grid = np.repeat(np.repeat(box_grid, 2, axis=0), 2, axis=1)
        grid_surf[box_grid] = BOX_COLOR

    grid_surf[grid] = LINE_COLOR

    img = Image.fromarray(np.rot90(grid_surf, 1), "RGB")
    img.save("mainPygameImage.png")