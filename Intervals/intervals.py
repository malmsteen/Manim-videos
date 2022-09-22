
from symbol import factor, namedexpr_test
from manim import *

import regex as re
import numpy as np
import string
import math
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve


class intervals(Scene):
    def construct(self):
        def change_plus(plus):
            c = plus.get_center()
            minus = MathTex('-', color=plus.get_color()).move_to(plus)
            self.play(FadeOut(plus), FadeIn(minus))
            return minus

        def substitute_x(formula, mob):
            svgs = formula[0]
            x_inds = [m.start() for m in re.finditer('x', f.get_tex_string())]
            x_svgs = [svgs[i] for i in x_inds]
            mobs = [mob.copy().animate.move_to(x).set_y(x.get_bottom()[1] + mob.height/2)
                    for x in x_svgs]
            self.play(
                *(FadeOut(x) for x in x_svgs),
                *mobs)
            return mobs

        ineq = [MathTex(s) for s in [
            '(x-{{1}})', '(x-({{-4}}))', '(x-{{3}})', '(x+{{1}})', '> 0']]
        ineq = Group(*ineq).arrange(RIGHT)
        f = MathTex('(x-1)(x+4)(x-3)(x+1) > 0 ').shift(UP)
        ixes = [m.start() for m in re.finditer('x', f.get_tex_string())]
        numbers = [m.start() for m in re.finditer(
            r'\d+', re.sub(' ', '', f.get_tex_string()))]
        for i in ixes:
            f[0][i].set_color(MONOKAI_GREEN)
        print(numbers)
        for i in numbers:
            f[0][i].set_color(MONOKAI_BLUE)

        numline = NumberLine(
            x_range=[-4, 4],
            length=10,
            include_ticks=False,
            include_tip=True,
            tip_width=.2,
            color=MONOKAI_YELLOW,
            z_index=2)\
            .next_to(ineq, DOWN, buff=1)
        # numline.add_labels({4: MathTex('x', font_size=36)})
        x_label = MathTex('x', color=MONOKAI_YELLOW).next_to(
            numline.n2p(4), DR, buff=.1)

        roots = [MathTex(n) for n in ['-4', '-{{1}}', '1', '3']]
        positions = [-2.5, -1, 1, 2.5]
        points = [-4, *positions, 4]
        signs = ['+', '-', '+', '-', '+']
        pairs = zip(signs, points[: -1], points[1:])
        total_signs = [MathTex(s).move_to(numline.n2p(.5*(p + q))).shift(.5*UP)
                       for s, p, q in pairs]
        colors = [MONOKAI_YELLOW, BLACK, MONOKAI_YELLOW, MONOKAI_YELLOW]
        circles = [Circle(radius=.07,
                          color=YELLOW_A,
                          fill_opacity=1,
                          fill_color=col,
                          stroke_width=1.5,
                          z_index=3)
                   .move_to(
            numline.n2p(n)) for n, col in zip(positions, colors)]

        labels = [root.next_to(numline.n2p(p), DOWN)
                  for root, p in zip(roots, positions)]

        # self.play(*(Write(i) for i in ineq))
        self.play(Write(f))
        self.play(Create(numline))
        self.play(Write(x_label))
        # self.play(
        #     LaggedStart(
        #         *(Create(circ) for circ in circles),
        #         lag_ratio=.2),
        #     LaggedStart(
        #         *(FadeIn(l) for l in labels),
        #         lag_ratio=.2)
        # )
        # pairs = [(0, 2), (1, 0), (2, 3), (3, 1)]
        # self.play(*(TransformMatchingTex(ineq[i].copy(), labels[j])
        #             for i, j in pairs))

        svgs = f[0]
        four = svgs[8].copy()
        one = svgs[18].copy()
        _four = MathTex(
            '-').add_updater(lambda m: m.next_to(four, LEFT, buff=.1))
        _four = Group(MathTex('-', color=four.get_color()
                              ).next_to(four, LEFT, buff=.1), four)
        _one = Group(MathTex('-', color=one.get_color()
                             ).next_to(one, LEFT, buff=.1), one)

        self.play(svgs[3].copy().animate.move_to(
            labels[2]), Create(circles[2]))
        self.play(FadeIn(_four[0]), _four.animate.move_to(
            labels[0]), Create(circles[0]))
        self.play(svgs[13].copy().animate.move_to(
            labels[3]), Create(circles[3]))
        self.play(FadeIn(_one[0]), _one.animate.move_to(
            labels[1]), Create(circles[1]))

        positions = [3, 2, 0, -2, -3]
        circles = [Circle(radius=.05,
                          color=MONOKAI_GREEN,
                          fill_opacity=1,
                          fill_color=MONOKAI_GREEN,
                          stroke_width=1.5,
                          z_index=3)
                   .move_to(numline.n2p(n))
                   for n in positions]
        probe_nums = [5, 2, 0, -2, -5]
        probes = [MathTex(pr, color=circles[0].get_color()).next_to(
            circ, DOWN).set_y(_one.get_y()) for pr, circ in zip(probe_nums, circles)]

        two = MathTex('2', color=circles[1].get_color()).next_to(
            circles[1], DOWN).set_y(_one.get_y())
        x_svgs = [svgs[i] for i in ixes]

        self.play(Create(circles[0]), FadeIn(probes[0]))

        fives = [probes[0].copy().animate.move_to(x).set_y(svgs[numbers[0]].get_y())
                 for i, x in enumerate(x_svgs)]
        factors_signs = ['++++', '+++-', '++--', '+---', '----']
        factors_signs = '++++'
        sign_places = [svgs[i+1].get_center() + .5*UP for i in ixes]
        factors_signs = [MathTex(s, color=MONOKAI_PINK).move_to(
            p) for s, p in zip(factors_signs, sign_places)]

        self.play(
            *(FadeOut(x) for x in x_svgs),
            *fives
        )
        self.wait(2)
        self.play(
            LaggedStart(
                *(FadeIn(s, shift=DOWN) for s in factors_signs),
                lag_ratio=.9,
                run_time=1
            )
        )
        self.wait(2)
        self.play(
            *(FadeIn(x) for x in x_svgs),
            *(f.move_to(probes[0]) for f in fives))

        self.play(
            *(Transform(s.copy(), total_signs[-1]) for s in factors_signs)
        )

        for i, num in enumerate([2, 0, 3, 1]):

            self.play(Create(circles[i+1]), FadeIn(probes[i+1]))
            mobs = substitute_x(f, probes[i+1])
            self.play(Wiggle(factors_signs[num]))
            factors_signs[num] = change_plus(factors_signs[num])
            self.wait()
            self.play(
                *(Transform(s.copy(), total_signs[-2-i]) for s in factors_signs)
            )
            self.wait()
            self.play(
                *(FadeIn(x) for x in x_svgs),
                *(f.move_to(probes[i+1]) for f in mobs)
            )

        # self.play(*(FadeOut(p) for p in factors_signs[0]),
        #           *(FadeIn(n) for n in factors_signs[1])
        #           )
        # self.play(*(FadeTransform(p, n)
        #             for p, n in zip(factors_signs[0], factors_signs[1])))
        # factors_signs[-1] = MathTex('-')

        self.wait(2)
