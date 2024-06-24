
from symbol import factor, namedexpr_test
from manim import *

import regex as re
import numpy as np
import string
import math
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve


class ideas(Scene):
    def construct(self):
        a = MathTex(r'\sqrt{x+2}', unpack_groups=False)
        b = MathTex('{{x}}^{{2}}')
        self.play(
            LaggedStart(*(
                        Indicate(s) for s in a[0]
                        ),
                        lag_ratio=1,
                        run_time=3
                        )
        )
        # self.play(TransformMatchingTex(a, b))
        self.wait(3)

        circ = Arc(angle=TAU, color=RED)
        rect = Rectangle()
        pp = (Dot(p) for p in circ.points)
        self.add(*pp)
        self.play(Create(circ))
        self.wait(3)

        vertices = [[-1, 1, 0], [0, 1, 0], [0, -1, 0], [1, -1, 0]]
        bcurve = CubicBezier(*[np.array(v) for v in vertices])
        self.play(Create(bcurve))
        self.wait()
