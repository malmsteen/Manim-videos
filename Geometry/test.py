from manim import *
import numpy as np
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve
import math


class tagentline(Scene):

    def tangent_from_point(self, p, circle, **kwargs):
        # self.add(Line(p, circle.get_center()))
        r = circle.radius
        cntr = circle.get_center()
        l = np.linalg.norm(cntr - p)
        theta = math.asin(r/l)
        c, s = math.cos(theta), math.sin(theta)
        R = np.array(([c, -s, 0], [s, c, 0], [0, 0, 1]))
        p1 = p + (R @ (cntr - p)/l) * r/math.tan(theta)
        return Line(p, p1, **kwargs)

    def construct(self):

        r = ValueTracker(1)
        c1 = LEFT+UP
        p = np.array([3, 2, 0])
        circ = always_redraw(lambda: Circle(
            radius=r.get_value(), color=MONOKAI_PINK).move_to(c1))
        tanLine = always_redraw(
            lambda: self.tangent_from_point(p, circ, color=MONOKAI_GREEN))

        self.play(Create(circ))
        self.wait(2)
        self.play(Create(tanLine))
        self.wait()
        self.play(r.animate.set_value(2))
        self.wait(2)
