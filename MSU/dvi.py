from turtle import down
from manim import *

import numpy as np
import string
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve


class planimetry(Scene):
    def tangent_circle(self, line, point, radius=1, d_alpha=1e-6, **kwargs):
        vec = line.get_vector()
        p1, p2 = point + vec*d_alpha, point - vec*d_alpha
        ext_point = line.get_start() + 3*LEFT
        # self.add(Dot(ext_point))

        return Circle.from_three_points(ext_point, p1, p2, **kwargs)

    def circle_line_intersection(self, circle, line, **kwargs):
        """Returns intersection points of line and a circle
        After test videos works propely
        """

        c = circle.get_center()
        r = circle.width/2
        p1, p2 = line.get_start(), line.get_end()
        x, y = symbols('x,y', real=True)
        line_vect = line.get_vector()
        print(c, r, p1, line_vect)
        # self.add(Dot(c))
        soln = nonlinsolve([(x-c[0])**2 + (y - c[1])**2 - r**2,
                            (x-p1[0])*line_vect[1] - (y - p1[1])*line_vect[0]],
                           [x, y])
        # tmp = [float(f) for tup in soln for f in tup]
        # self.play(Create(Dot(x1)), Create(Dot(x2)))
        # print(type(x1), x2)
        # print(type(soln[1]))
        print(soln)
        lst = [[float(tup[0]), float(tup[1]), 0] for tup in soln]
        print(lst)
        return lst[1]

    def make_hint(self, mob):
        bg = BackgroundRectangle(
            mob, color=GRAY, stroke_width=0, fill_opacty=.3, radius=.3)

    def construct(self):
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        """)
        MathTex.set_default(tex_template=tmpl, font_size=28)
        Dot.set_default(fill_opacity=0)

        text = Tex(
            r'Окружность, проходящая через вершину $A$ треугольника $A B C$, касается его стороны $B C$ в точке $D$ и пересекает стороны $A C$ и $A B$ в точках $E$ и $F$ соответственно. Известно, что $A F=3 B F$, $B D=C D, A E=2 C E$ и что $E D=\sqrt{10}$. Найдите $B C$.')

        circle = Circle(radius=1, color=MONOKAI_PINK).shift(RIGHT)
        # bc = TangentLine(circle, alpha=.13, length=3, color=MONOKAI_BLUE)

        c = 2*RIGHT
        b = Dot(1.5*RIGHT + 3 * UP)
        a = c + 3 * LEFT
        cb = always_redraw(lambda: Line(c, b.get_center(), color=MONOKAI_BLUE))
        # ab = always_redraw(lambda: Line(a, b), color=MONOKAI_BLUE)
        d = always_redraw(lambda: Dot(
            midpoint(b.get_center(), c)))
        tancirc = always_redraw(
            lambda: self.tangent_circle(cb, d.get_center(), color=MONOKAI_PINK))
        line1 = Line(DOWN, UP+RIGHT)
        print("tancirc.radius: ", tancirc.radius, tancirc.width/2)
        ca = Line(c, a, color=MONOKAI_BLUE)
        ab = Line(a, b)
        e = Dot(self.circle_line_intersection(tancirc, ca))
        f = Dot(self.circle_line_intersection(tancirc, ab))
        de = always_redraw(lambda: Line(d.get_center(), e.get_center(),
                                        color=MONOKAI_BLUE, z_index=-1))
        abc = always_redraw(lambda: Polygram(
            [a, c, b.get_center()], color=MONOKAI_BLUE))

        def mymidpoint(p1, p2):
            if type(p1) != np.ndarray:
                p1 = p1.get_center()
            if type(p2) != np.ndarray:
                p2 = p2.get_center()
            # for p in {p1, p2}:
            #     if type(p) != np.ndarray:
            #         p = p.get_center()
            return midpoint(p1, p2)

        # calculating final intersections of circle and sides of triangle ABC
        bprime = [ca.get_x(), b.get_y(), 0]
        m = midpoint(c, bprime)
        # print(type(m))
        circprime = self.tangent_circle(Line(c, bprime), m)
        eprime = self.circle_line_intersection(circprime, ca)
        fprime = self.circle_line_intersection(circprime, Line(a, bprime))

        self.play(Create(abc))
        # self.play()
        self.add(cb, Dot(a), Dot(c), b, d, e, f)
        self.play(Create(tancirc))
        self.play(Create(de))
        self.wait()
        # eprime = self.circle_line_intersection(tancirc, ca)
        # fprime = self.circle_line_intersection(tancirc, Line(a, b))
        # self.play(FadeIn(eprime), FadeIn(fprime))
        # circ1 = Circle(radius=tancirc.radius, color=MONOKAI_GREEN).move_to(
        #     tancirc.get_center())
        # print(circ1.radius, circ1.width)
        # line1 = Line().shift(UP).rotate(TAU/8)
        # p1 = self.circle_line_intersection(circ1, line1)

        # writing vertcies and marks
        # b, d,  e, f = [v.get_center() for v in [b, d, e, f]]
        vertices = [a, b, c, d, e, f]
        for v in vertices:
            print(type(v), '\n')
        # vertices = [v if type(v) != Dot else v.get_center()
        #             for v in [a, b, c, d, e, f]]
        tos = [DL, UR, DR, RIGHT, DOWN, LEFT]

        middles = [(b, d), (c, d), (b, f), (f, a), (c, e), (a, e)]
        marks = ['a', 'a', 'x', '2x', 'y', '2y']
        mark_tos = [RIGHT, RIGHT, UL, UL, DOWN, DOWN]

        letters = []
        for l, v, to in zip(string.ascii_uppercase, vertices, tos):
            def func(m, v=v, to=to):
                return m.next_to(v, to, buff=.1)
            letters.append(MathTex(l).add_updater(func))
        self.play(
            LaggedStart(
                *(Write(l) for l in letters),
                lag_ratio=.3,
                run_time=1.5
            )
        )

        marksxy = []
        for mark, mid, to in zip(marks, middles, mark_tos):
            def func(m, mid=mid, to=to):
                return m.next_to(mymidpoint(*mid), to, buff=.1)
            marksxy.append(MathTex(mark, color=YELLOW_D).add_updater(func))

        self.play(*(Write(m) for m in marksxy))
        self.add(tancirc)
        letters[-2].clear_updaters()
        letters[-1].clear_updaters()
        self.play(b.animate.set_x(ca.get_x()),
                  letters[-2].animate.next_to(eprime, DOWN, buff=.1),
                  letters[-1].animate.next_to(fprime, UL, buff=.1),
                  e.animate.become(Dot(eprime)),
                  f.animate.become(Dot(fprime)),
                  run_time=3)
        # eprime = self.circle_line_intersection(tancirc, ca)
        # fprime = self.circle_line_intersection(tancirc, Line(a, b))
        self.play(FadeIn(Dot(eprime)), FadeIn(Dot(fprime)))
        # self.play(cb.animate.rotate(-TAU/4))

        # cir = Circle(radius=2)
        # lin = Line([3, 2, 0], [-4, -1, 0])
        # self.play(Create(cir))
        # p1, p2 = always_redraw(lambda: self.circle_line_intersection(cir, lin))
        # self.play(Create(lin), Write(p1), Write(p2))
        # self.play(lin.animate.shift(DOWN))

        # dots1 = self.circle_line_intersection(tancirc, line)
        # self.add(dots1)
        # print(type(dots[0]))
        # self.play(*(Create(Dot(d)) for d in dots))
        # self.play(Create(Line(*dots)))
        self.wait(2)
