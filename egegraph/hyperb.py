from scipy.interpolate import lagrange
from manim import *

import regex as re
import numpy as np
import math
import sys
import os
from colors import *

graph_style_dict = {
    'axis_config':  {"include_numbers": False,
                     'tip_shape': StealthTip},
    'y_axis_config': {"label_direction": LEFT,
                      "numbers_to_include": [0, 1]},
    'x_axis_config': {"label_direction": DOWN,
                      "numbers_to_include": [1]},
    'background_line_style': dict(
        stroke_width=1,
        stroke_opacity=.6
    )
}

PI = math.pi

class Hyperb(Scene):
    def construct(self):


        plane = NumberPlane(
            x_range=(-7.2, 7.2),
            y_range=(-7.2, 7.2),
            x_length=4,
            y_length=4,
            **graph_style_dict,
        )
        plane.shift(4*RIGHT)
        # color = #0FF1CE"
        def fun(x): return 2/(x+2)

        k = ValueTracker(1)
        graph0 = always_redraw(
            lambda:
            plane.plot(
            lambda x: k.get_value()/x,
            color = "#0ff1ce",
            x_range=(-7.2, 7.2),
            discontinuities = [0],
            dt = k.get_value()/7.2
            )
        )
        # graph0.always_redraw()

        graph1 = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-1.62, 5.2)
        )
        graph2 = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-5.2, -2.38)
        )
        asymptote = DashedLine(
            plane.get_top(),
            plane.get_bottom(),
            color=MONOKAI_BLUE,
            stroke_width=1.5
        )
        asymptote.set_x(plane.c2p(-2, 0)[0])
        # x = [-4]
        # y = [fun(x) for x in x]

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph0))
        self.wait()
        # self.play(Create(asymptote))
        # self.play(Create(graph1), Create(graph2))
        # self.wait(2)

        self.play(k.animate.set_value(10), rate_func = there_and_back, run_time=4 )
        self.wait()

        self.play(Rotate(graph0, angle = PI, axis = RIGHT), rate_func= there_and_back_with_pause, run_time = 5)
        self.wait()

        hyp = MathTex("{{y}}","=","{","{{k}}",r"\over","{{x}}","}")
        alt = MathTex('{{x}}','{{y}}',"=", "{{k}}")
        self.play(Write(hyp))
        self.play(TransformMatchingTex(hyp,alt))
        p1 = MathTex('(x_0, y_0)')
        p2 = MathTex('(y_0, x_0)')
        r = 0.05

        d1 = Dot(plane.c2p(3,1/3),radius = r)

        d2 = Dot(plane.c2p(1/3,3),radius = r)

        a = 7
        y_eq_x = DashedLine(
            plane.c2p(-a,-a),
            plane.c2p(a,a),
            color = MONOKAI_BLUE,
            stroke_width = 1.5)
        self.play(Create(y_eq_x), FadeIn(d1), FadeIn(d2))
        self.wait()
        self.play(FadeOut(y_eq_x))

        asym1 = DashedLine(
            plane.get_top(),
            plane.get_bottom(),
            color=MONOKAI_PINK,
            stroke_width=1.5
        )

        asym2 = DashedLine(
            plane.get_left(),
            plane.get_right(),
            color=MONOKAI_PINK,
            stroke_width=1.5
        )
        self.play(Create(asym1), Create(asym2))
        self.wait()
        self.play(Uncreate(asym1), Uncreate(asym2), FadeOut(d1, d2))
        self.wait(3)

        graph0.clear_updaters()
        f1 = MathTex(r'y = \frac{1}{x-3}')

        self.play(graph0.animate.shift(plane.c2p(3,0) - plane.c2p(0,0)))
        self.wait()
        self.play(Create(asym1.set_x(plane.c2p(3,0)[0])))
        self.wait()






        # self.play(
        #     LaggedStart(
        #         *(FadeIn(
        #             Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
        #           for abs, ord in zip(x, y)
        #           ),
        #         lag_ratio=.4
        #     )
        # )
        # self.wait(2)

        # texts = [
        #     r'f(x) = \frac{k}{x+a}, \quad f(-7)= ?'
        # ]
