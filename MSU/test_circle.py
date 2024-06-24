
from turtle import down
from manim import *

import numpy as np
import string
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve


class example(Scene):

    def circle_line_intersection(self, circle, line, **kwargs):
        """Returns intersection points of line and a circle
            After test videos works propely
            """

        c = circle.get_center()
        r = circle.width/2
        p1, p2 = line.get_start(), line.get_end()
        x, y = symbols('x,y', real=True)
        line_vect = line.get_vector()
        # print(c, r, p1, line_vect)
        self.add()
        soln = nonlinsolve([(x-c[0])**2 + (y - c[1])**2 - r**2,
                            (x-p1[0])*line_vect[1] - (y - p1[1])*line_vect[0]],
                           [x, y])
        # tmp = [float(f) for tup in soln for f in tup]
        # self.play(Create(Dot(x1)), Create(Dot(x2)))
        # print(type(x1), x2)
        # print(type(soln[1]))
        # print(soln)
        lst = [[float(tup[0]), float(tup[1]), 0] for tup in soln]
        # print(lst)
        return lst[1]

    def construct(self):

        circ = Circle(radius=2)
        line = Line(4*LEFT, 2*RIGHT+UP)

        d = Dot().add_updater(lambda m: m.move_to(self.circle_line_intersection(circ, line)))
        self.play(Create(circ))
        self.play(Create(line))
        self.play(FadeIn(d))
        self.wait()
        self.play(circ.animate.become(Circle(radius=1)))
        self.wait(2)
