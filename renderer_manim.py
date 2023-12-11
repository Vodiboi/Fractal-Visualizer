from manim import *
from typing import *
import numpy as np
import mathstuff
import mathInfo

def transform(pt:complex, r:int, theta:int, shift:complex) -> complex:
    '''
    transforms pt by scale `r`, angle `theta` and shift `shift`
    '''
    return (r*pt.real*np.cos(theta)-r*pt.imag*np.sin(theta)) + (r*pt.real*np.sin(theta)+r*pt.imag*np.cos(theta))*1j + shift


USEPOINTS = 1
LINES = mathstuff.recursively_subdivide(mathInfo.START, mathInfo.END, mathInfo.NUM_RECURSIONS)
if len(LINES) > 7000:
    raise ValueError(f"Too Many Lines To Render: {len(LINES)}")

SCALE:int = 1
THETA:int = 0
SHIFT:complex = 0

class TestScene(Scene):
    # generates the scene
    def construct(self):
        global SCALE, SHIFT, LINES, THETA
        p = ComplexPlane()
        p.add_coordinates()
        self.add(p)
        for p1, p2 in LINES:
            self.add(Line(p.n2p(transform(p1, SCALE, THETA, SHIFT)), p.n2p(transform(p2, SCALE, THETA, SHIFT))))

