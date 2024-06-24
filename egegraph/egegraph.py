
from scipy.interpolate import lagrange
from manim import *

import regex as re
import numpy as np
import math
import sys
import os
from colors import *

sys.path.append(os.path.abspath("~/Desktop/Manim_video"))
# import local_colors
os.system("python ../local_colors.py")


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


class ParabolaInt(Scene):
    def construct(self):
        ax = Axes().add_coordinates()
        plane = NumberPlane(
            x_range=(-2, 6),
            y_range=(-4, 6),
            x_length=4,
            y_length=4*10/8,
            **graph_style_dict
        )

        def fun(x): return (x-4)**2 - 3
        parabola = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(1, 5.6)
        )
        p1 = plane.c2p(3, -2)
        p2 = plane.c2p(5, -2)

        self.play(Create(plane))
        self.wait()
        self.play(Create(parabola))
        self.wait(2)

        texts = ['f(x)= ax^2 + bx+ c, \quad f(-5) = ?',
                 'a=1',
                 'f(x) = (x-4)**2 - 3',
                 'f(-5) = 78']
        texts = VGroup(*[MathTex(t) for t in texts])

        texts.arrange(DOWN).shift(3*LEFT + UP)

        self.play(Write(text1),
                  plane.animate.shift(4*RIGHT),
                  parabola.animate.shift(4*RIGHT))
        self.wait(2)

        vertex = Dot(plane.c2p(4, -3), color=MONOKAI_BLUE, radius=.05)
        lineHoriz = Line(plane.get_right(), plane.get_left())
        lineHoriz\
            .align_to(vertex)\
            .set_y(vertex.get_y())\
            .set(
                color=MONOKAI_GREEN,
                stroke_width=.5,
            )\
            .set_z_index(-1)

        lineVert = Line(plane.get_top(), plane.get_bottom())
        lineVert\
            .align_to(vertex)\
            .set_x(vertex.get_x())\
            .match_style(lineHoriz)
        # local_plane = plane.axes.copy().shift(vertex - plane.c2p(0, 0))
        # local_plane.set(
        #     axis_config={'include_numbers': False},
        #     color=GREEN,
        #     opcity=.5)
        self.play(FadeIn(vertex),
                  FadeIn(lineHoriz))
        self.play(FadeIn(lineVert))
        self.wait(3)

        t1 = ValueTracker(4)
        t2 = ValueTracker(4)
        vertex1 = vertex.copy()
        vertex1.add_updater(lambda x: x.move_to(
            plane.c2p(t1.get_value(), fun(t1.get_value()))))
        vertex2 = vertex.copy()
        vertex2.add_updater(lambda x: x.move_to(
            plane.c2p(t2.get_value(), fun(t2.get_value()))))

        self.add(vertex1, vertex2)
        self.play(t1.animate.set_value(5), t2.animate.set_value(3))
        self.wait(2)


class Parabola(Scene):
    def construct(self):

        plane = NumberPlane(
            x_range=(-2, 7),
            y_range=(-5, 6),
            x_length=4,
            y_length=4*11/9,
            **graph_style_dict
        )
        plane.shift(4*RIGHT)

        x = [3, 4, 5]
        y = [-1, -4, -3]
        fun = lagrange(x, y)

        parabola = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(1.95, 6.5)
        )

        self.play(Create(plane))
        self.wait()
        self.play(Create(parabola))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x, y)
                  ),
                lag_ratio=.2
            )
        )
        self.wait(2)

        texts = [
            'f(x)= ax^2 + bx+ c, \quad c = ?',
            r'''\left\{ \begin{array}{l}
            -1 = 9a + 3b + c\\
            -4 = 16a + 4b +c\\
            -5 = 25a + 5b +c
            \end{array} \right.''',
            '0 = 2b + c',
            r'''\left\{ \begin{array}{l}
                -1 = 9a - \frac32 c + c\\
                -4 = 16a -2c +c
                \end{array} \right.''',
            r'''\left\{ \begin{array}{l}
                -2 = 18a -c\\
                -4 = 16a -c
                \end{array} \right.
            ''',
            '   a = 1', 'c = 20.']


class ParabolaTwoCoefs(Scene):
    def construct(self):

        plane = NumberPlane(
            x_range=(-3, 3),
            y_range=(-8, 2),
            x_length=4,
            y_length=4*10/6,
            **graph_style_dict
        )
        plane.shift(4*RIGHT)

        x = [-1, 2, 1]
        y = [-4, -1, -6]
        fun = lagrange(x, y)

        parabola = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-1.8, 2.2)
        )

        self.play(Create(plane))
        self.wait()
        self.play(Create(parabola))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.075))
                  for abs, ord in zip(x[:-1], y[:-1])
                  ),
                lag_ratio=.2
            )
        )
        self.wait(2)

        texts = [
            'f(x) = 2x^2 + bx + c, \quad f(-6) = ?',
            r'''\left\{ \begin{array}{l}
            -4 = 2 -b + c\\
            -1 = 8 + 2b + c
            \end{array} \right.
            ''',
            'c = -7, b = -1, f(-6) = 71'
        ]

        texts = VGroup(*[MathTex(t) for t in texts])
        texts.arrange(DOWN).shift(3*LEFT + UP)

        for t in texts:
            self.play(Write(t))

        self.wait(2)


class Log(Scene):  # V10
    def construct(self):

        plane = NumberPlane(
            x_range=(-5.1, 5.1),
            y_range=(-5.1, 5.1),
            x_length=4,
            y_length=4,
            **graph_style_dict
        )
        plane.shift(4*RIGHT)

        def fun(x): return 2*math.log(x+3, 2)

        graph = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-2.85, 3.1)
        )

        x = [-2, 1]
        y = [0, 4]

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x, y)
                  ),
                lag_ratio=.4
            )
        )
        self.wait(2)


class Exp(Scene):  # V27
    def construct(self):

        plane = NumberPlane(
            x_range=(-5.2, 5.2),
            y_range=(-5.2, 5.2),
            x_length=4,
            y_length=4,
            **graph_style_dict
        )
        plane.shift(4*RIGHT)

        def fun(x): return 3**x - 5

        graph = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-2.85, 2.1)
        )

        x = [0, 1]
        y = [fun(x) for x in x]

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x, y)
                  ),
                lag_ratio=.4
            )
        )
        self.wait(2)


class ParabolaLine(Scene):  # V 15
    def construct(self):
        plane = NumberPlane(
            x_range=(-5.2, 5.2),
            y_range=(-5.2, 5.2),
            x_length=4,
            y_length=4,
            **graph_style_dict
        )
        plane.shift(4*RIGHT)

        x1 = [-2, 0, 1]
        y1 = [-2, -4, 1]
        Gparabola = lagrange(x1, y1)

        x2 = [-2, -1]
        def line(x): return 4*x + 6
        y2 = [line(x) for x in x2]

        graph1 = plane.plot(
            parabola,
            color=pastel_orange,
            x_range=(-3, 1.5)
        )

        graph2 = plane.plot(
            line,
            color=pastel_orange,
            x_range=(-3, -.2)
        )

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph1))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x1, y1)
                  ),
                lag_ratio=.4
            )
        )
        self.play(Create(graph2))
        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x2, y2)
                  ),
                lag_ratio=.4
            )
        )
        self.wait(2)

        texts = [
            'f(x) = ax^2 + bx + c, \, g(x) = kx + d'
        ]


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
        x = [-4]
        y = [fun(x) for x in x]

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph0))
        self.wait()
        # self.play(Create(asymptote))
        # self.play(Create(graph1), Create(graph2))
        # self.wait(2)

        self.play(k.animate.set_value(10), rate_func = there_and_back, run_time=2)
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


class Trigonometry(Scene):  # V33
    def construct(self):
        graph_style_dict['axis_config']['include_numbers'] = False
        plane = NumberPlane(
            x_range=(-5.2, 5.2),
            y_range=(-5.2, 5.2),
            x_length=4,
            y_length=4,
            **graph_style_dict,
        )
        plane.shift(4*RIGHT)

        def fun(x): return 2/(x+2)

        graph = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-5.2, 5.2)
        )

        x = [-4]
        y = [fun(x) for x in x]

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x, y)
                  ),
                lag_ratio=.4
            )
        )
        self.wait(2)


class Sqrt(Scene):
    def construct(self):

        plane = NumberPlane(
            x_range=(-5.2, 5.2),
            y_range=(-5.2, 5.2),
            x_length=4,
            y_length=4,
            **graph_style_dict,
        )
        plane.shift(4*RIGHT)

        def fun(x): return 1.5 * math.sqrt(x + 2)

        graph = plane.plot(
            fun,
            color=pastel_orange,
            x_range=(-2, 5.2)
        )

        x = [-2, 2]
        y = [fun(x) for x in x]

        self.play(Create(plane))
        self.wait()
        self.play(Create(graph))
        self.wait(2)

        self.play(
            LaggedStart(
                *(FadeIn(
                    Dot(plane.c2p(abs, ord), color=MONOKAI_BLUE, radius=.05))
                  for abs, ord in zip(x, y)
                  ),
                lag_ratio=.4
            )
        )
        self.wait(2)

        text = [
            'f(x)=k\sqrt{x+p}, \quad f(-0,25) = ?'
        ]
