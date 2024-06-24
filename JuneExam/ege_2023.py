
from manim import *
import regex as re
import numpy as np
import math
import sys
import os


sys.path.append(os.path.abspath("~/Desktop/Manim_video"))
# import local_colors
os.system("python ../local_colors.py")

pastel_background = "#2e2e2e"
pastel_comments = "#797979"
pastel_white = "#d6d6d6" "#ffd76d"
pastel_yellow = "#e5b567"
pastel_green = "#b4d273"
pastel_orange = "#e87d3e"
pastel_purple = "#9e86c8"
pastel_pink = "#b05279"
pastel_blue = "#6c99bb"

MONOKAI_PINK = '#f92672'
MONOKAI_ORANGE = '#fd971f'
MONOKAI_YELLOW = '#e6da74'
MONOKAI_BLUE = '#66d9ef'
MONOKAI_GREEN = '#a6e22e'
MONOKAI_PURPLE = '#ae81ff'
MONOKAI_GRAY = '#272822'
MONOKAI_LIGHTGRAY = '#74715e'
MONOKAI_WHITE = '#f6f6f6'


tmpl = TexTemplate()
tmpl.add_to_preamble(r"""
\usepackage{mathtext}
\usepackage[T2A]{fontenc}
\usepackage[utf8]{inputenc}
%\usepackage[english,russian]{babel}
""")


graph_style_dict = {
    'axis_config':  {"include_numbers": False,
                     'tip_shape': StealthTip,
                     'line_to_number_buff': .1},
    'y_axis_config': {"label_direction": UL,
                      "numbers_to_include": [0, 1]},
    'x_axis_config': {"label_direction": DR,
                      "numbers_to_include": [1]},
    # 'background_line_style': dict(
    #     stroke_width=1,
    #     stroke_opacity=.6
    # )
}


class Equation(Scene):
    def construct(self):

        MathTex.set_default(tex_template=tmpl, font_size=28)
        soln1 = [
            r'\left[-3 \pi; -\frac{5 \pi}{2}\right]',
            r'2 \cos x ( \cos^2 x - 1) - \sqrt3 \sin^2 x = 0',
            r'-2 \cos x \sin^2 x - \sqrt3 \sin^2 x = 0',
            r'\sin^2 x (2 \cos x + \sqrt3) \ =0',
            r'''
            \left[ \begin{array}{l}
            \sin x = 0,\\
            \cos x = -\frac{\sqrt3}{2}
            \end{array} \right.
            ''',
            r'''
            \left[ \begin{array}{l}
            x = \pi n,\\
            x = \pm \frac {5 \pi}{6} + 2 \pi n
            \end{array} \right.,
            n \in \mathbb{Z}

            ''',
        ]

        problem1 = VGroup(
            MathTex(
                r'\text{ Решите уравнение: } 2 \cos ^ 3 x =\sqrt{3} \sin ^ 2 x+2 \cos x'),
            MathTex(r'\text{ и укажите все решения из отрезка } \left[-3 \pi; -\frac{3 \pi}{2}\right]'))\
            .arrange(DOWN)\
            .scale(1.2)\
            .to_edge(UP)\
            .set_color(MONOKAI_YELLOW)
        soln1 = VGroup(
            *(MathTex(t, color=pastel_white)  # , substrings_to_isolate='x').set_color_by_tex("x", pastel_green)
              for t in soln1[1:])).arrange(DOWN).next_to(problem1, DOWN, buff=1)
        bgrect = BackgroundRectangle(
            problem1,
            color=DARK_GRAY,
            corner_radius=.2,
            buff=.2
        )

        self.play(FadeIn(bgrect))
        self.play(Write(problem1))
        self.wait()

        for s in soln1:
            self.play(Write(s))
            self.wait()

        self.wait(2)

        sur = SurroundingRectangle(soln1[-1], color=MONOKAI_BLUE)
        self.play(ShowPassingFlash(sur, run_time=2, time_width=.8),
                  soln1[-1].animate.set_color(MONOKAI_BLUE))
        self.wait()

        self.play(soln1.animate.shift(3*LEFT))
        self.wait()

        plane = Axes(
            x_range=(-2, 2),
            y_range=(-2, 2),
            x_length=4,
            y_length=4,
            ** graph_style_dict
        ).next_to(soln1, RIGHT, buff=2)

        self.play(Create(plane))
        self.wait()
        circ = Circle().move_to(plane)
        self.play(Create(circ))
        self.wait()
        # arc1 = Arc(start_angle=-PI, angle=1.5*PI,
        #            color=MONOKAI_BLUE, stroke_width=4).move_to(plane)
        arc1 = circ.get_subcurve(.5, .25,)
        arc1.set_color(MONOKAI_BLUE)

        self.play(Create(arc1))
        self.wait()
        pp = [Dot(circ.point_at_angle(ang), radius=.05)
              for ang in [0, PI, 5*PI/6, -5*PI/6]]
        self.play(
            LaggedStart(
                *(FadeIn(p) for p in pp[:2]),
                lag_ratio=.5
            )
        )
        self.play(
            FadeIn(MathTex(
                r'-\frac{\sqrt 3}{2}', font_size=24, color=MONOKAI_BLUE).next_to(plane.c2p(-math.cos(PI/6), 0), UR, buff=.1)),
            Create(DashedLine(pp[2], pp[3], color=MONOKAI_BLUE, stroke_width=1.5)))
        self.play(FadeIn(pp[2]), FadeIn(pp[3]))
        self.wait()

        directions = [UR, UL, UL, DL]

        roots = [r'-3 \pi', r'-2 \pi',
                 r'-3 \pi -\frac{\pi}{6}', r'-3\pi + \frac{\pi}{6}']
        roots = [MathTex(r, font_size=28) for r in roots]

        self.play(
            LaggedStart(
                *(Write(r.next_to(p, d, buff=.1))
                  for r, p, d in zip(roots, pp, directions)),
                lag_ratio=.5
            )
        )
        self.wait()
        ansB = MathTex(r'-3 \pi, -2 \pi, -\frac{19 \pi}{6}, -\frac{17\pi}{6}')
        ansB.next_to(soln1, DOWN)
        self.play(Write(ansB))

        sur = SurroundingRectangle(ansB, color=MONOKAI_BLUE)
        self.play(ShowPassingFlash(sur, run_time=2, time_width=.8),
                  ansB.animate.set_color(MONOKAI_BLUE))

        allMobs = VGroup(soln1, circ, arc1, plane, *pp, *roots)
        sol = [mob for mob in self.mobjects if mob not in {problem1, bgrect}]
        # sol = sol.pop(problem1)
        self.play(FadeOut(*sol))
        self.wait(2)

        eqn2 = [r'2 \sin ^3 x+\sqrt{2} \cos ^2 x=2 \sin x',
                r'\left[-3 \pi ;-\frac{3 \pi}{2}\right]'
                ]

        problem2 = VGroup(
            MathTex(r'\text{ Решите уравнение: }' + f'{eqn2[0]}'),
            MathTex(
                r'\text{ и укажите все решения из отрезка }' + f'{eqn2[1]}'))\
            .arrange(DOWN)\
            .scale(1.2)\
            .next_to(problem1, DOWN, buff=1)\
            .match_style(problem1)

        self.play(FadeIn(bgrect.copy().move_to(problem2)))
        self.play(Write(problem2))
        self.wait(2)


class Inequality(Scene):
    def make_shade(cls, p1, p2):
        vec = p2-p1
        vec_len = np.linalg.norm(vec)
        unit_vec = vec/vec_len
        direction = angle_between_vectors(vec, RIGHT)
        angle = TAU/6
        dl = .15

        l = .2

        def prime():
            return Rectangle(width=l,
                             height=.05,
                             stroke_width=0,
                             fill_color=MONOKAI_BLUE,
                             fill_opacity=1,)\
                .move_to(p1)\
                .rotate(direction + angle)\
                .shift(l/2 * rotate_vector(unit_vec, angle))
        # print(vec_len, angle)
        shade = [prime().shift(unit_vec*i)
                 for i in np.arange(dl, vec_len-dl, dl)
                 ]

        # print(type(shade))
        return shade

    def construct(self):

        MathTex.set_default(tex_template=tmpl, font_size=28)
        ineq1 = [
            r'\left(\log _{0,25}^2(x+3)-\log _4\left(x^2+6 x+9\right)+1\right) \cdot \log _4(x+2) \leqslant 0']
        ineq2 = [
            r'\log _{25}\left((x-4)\left(x^2-2 x-8\right)\right)+1 \geqslant 0,5 \log _5(x-4)^2']
        ineq3 = [
            r'\log_{0,1}(x^3 - 5x^2-25x+125) \leqslant \log_{0,01}(x-5)^4']
        ineq4 = [
            r'\frac{\log_3(3-x) - \log_2 (x+2)}{\log^2_3x^2 + \log_3 x^4 + 1} \geqslant 0']

        domain1 = [
            MathTex(r'\text{ОДЗ: }'),
            MathTex(r'''\left\{ \begin{array}{l}
            x + 3 > 0\\
            x^2 + 6x + 9 > 0\\
            x + 2 > 0
            \end{array} \right.
            '''),
            MathTex(r'''\left\{ \begin{array}{l}
            x > -3\\
            (x+3)^2 > 0\\
            x > -2
            \end{array} \right.
            '''),
            MathTex('x > -2')
        ]
        domain1 = VGroup(*domain1)\
            .arrange(DOWN, aligned_edge=LEFT)\
            .to_edge(RIGHT)

        soln1 = [
            r'(\log^2_4(x+3) - 2 \log_4(x+3) + 1) \cdot \log_4 (x+2) \leqslant 0',
            r'(\log_4(x+3) -1)^2 \log_4 (x+2) \leqslant 0']
        soln1 = VGroup(*[MathTex(f) for f in soln1])
        hint1 = [r'\log_{\frac14}(x+3) = -\log_4 (x+3)',
                 r'\log_4(x+3)^2 = 2\log_4|x+3|']

        problem1 = MathTex(*ineq1)\
            .scale(1.2)\
            .to_edge(UP)\
            .set_color(MONOKAI_YELLOW)
        bgrect = BackgroundRectangle(
            problem1,
            color=DARK_GRAY,
            corner_radius=.1,
            buff=.2
        )
        soln1.arrange(DOWN).next_to(problem1, DOWN, buff=1)

        self.play(FadeIn(bgrect))
        self.play(Write(problem1))
        self.wait()
        self.play(Write(domain1))
        self.wait()
        self.play(Write(soln1[0]))
        self.wait()
        self.play(Write(soln1[1]))
        self.wait()

        numline = NumberLine(
            x_range=[-3, 3],
            length=5,
            include_ticks=False,
            include_tip=True,
            tip_width=.2,
            color=MONOKAI_YELLOW,
        )\
            .next_to(soln1[1], DOWN, buff=1)\
            # .add_labels('x')
        numline.add_labels(
            {3: MathTex('x', font_size=36), })
        x_label = MathTex('x', color=MONOKAI_YELLOW).next_to(
            numline.n2p(4), DR, buff=.1)

        signs = '-++'
        pp = [-1, 1]
        dots = [Dot(numline.n2p(p), radius=.06) for p in pp]
        labels = [MathTex(str(l)).next_to(d, DOWN) for l, d in zip(pp, dots)]

        pointsOnline = [numline.n2p(p)for p in [-3]+pp+[3]]
        pairs = zip(pointsOnline[: -1], pointsOnline[1:])

        self.play(Create(numline))
        self.play(
            *(FadeIn(d) for d in dots),
            *(FadeIn(l) for l in labels))

        signsOnline = [MathTex(s).move_to(.5*(
            p[0] + p[1]) + .5*UP) for s, p in zip(signs, pairs)]

        self.play(*(FadeIn(s) for s in signsOnline))
        self.wait(3)

        p1, p2 = pointsOnline[0:2]
        shade = self.make_shade(p1, p2)
        self.play(
            LaggedStart(
                *(Create(s) for s in shade),
                lag_ratio=.3,
                run_time=1
            ))
        self.play(dots[1].animate.set_color(MONOKAI_BLUE))
        self.wait(2)

        pic = Group(*[mob for mob in self.mobjects if mob not in {
            problem1, bgrect, soln1}])
        pic = Group(*shade, numline, *labels, *signsOnline, *dots)
        # self.play(pic.animate.shift(2*RIGHT))
        self.wait(2)

        # sol = sol.pop(problem1)


class Parameter(Scene):
    def construct(self):

        param1 = [
            r'''
            \left\{\begin{array}{l}
            (x y-x+8) \cdot \sqrt{y-x+8}=0
            y=2 x+a
            \end{array}\right.
            '''
        ]

        param2 = [
            r'''
            \left\{\begin{array}{l}
            (x ^ 2 + y ^ 2 + 6x) \sqrt{x+y+6}=0
            y=x + a
            \end{array} \right.
            '''
        ]

        param4 = [
            r'''
            \left\{\begin{array}{l}
            (x ^ 2-7x + 8 - y) \sqrt{x-y + 8}
            y=ax + a
            \end{array} \right.
            '''
        ]
