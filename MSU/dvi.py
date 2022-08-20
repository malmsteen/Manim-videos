from manim import *

import numpy as np
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve


def tangent_circle(line, point, radius=1, d_alpha=1e-6, **kwargs):
    vec = line.get_vector()
    p1, p2 = point + vec*d_alpha, point - vec*d_alpha
    ext_point = line.get_start() + LEFT

    return Circle.from_three_points(ext_point, p1, p2, **kwargs)


class planimetry(Scene):
    def tagent_circle(self, circle, line):
        pass

    def circle_line_intersection(self, circle, line, **kwargs):
        """returns intersection points of line and a circle"""

        c = circle.get_center()
        r = circle.radius
        x1, x2 = line.get_start(), line.get_end()
        x, y = symbols('x,y', real=True)
        line_vect = line.get_vector()
        print(c, r, x1, line_vect)
        soln = nonlinsolve([(x-c[0])**2 + (y - c[1])**2 - r**2,
                            (x-x1[0])*line_vect[1] - (y - x1[1])*line_vect[0]],
                           [x, y])
        # tmp = [float(f) for tup in soln for f in tup]
        # self.play(Create(Dot(x1)), Create(Dot(x2)))
        # print(type(x1), x2)
        # print(type(soln[1]))
        print(type(soln))
        return [[float(tup[0]), float(tup[1]), 0] for tup in soln]

    def make_hint(self, mob):
        bg = BackgroundRectangle(
            mob, color=GRAY, stroke_width=0, fill_opacty=.3, radius=.3)

    def construct(self):
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        \usepackage[english,russian]{babel}""")
        MathTex.set_default(tex_template=tmpl, font_size=28)

        # text = Tex(
        #     r'Окружность, проходящая через вершину $A$ треугольника $A B C$, касается его стороны $B C$ в точке $D$ и пересекает стороны $A C$ и $A B$ в точках $E$ и $F$ соответственно. Известно, что $A F=3 B F$, $B D=C D, A E=2 C E$ и что $E D=\sqrt{10}$. Найдите $B C$.')

        circle = Circle(radius=1, color=MONOKAI_PINK).shift(RIGHT)
        # bc = TangentLine(circle, alpha=.13, length=3, color=MONOKAI_BLUE)

        b = Point(RIGHT + 3 * UP)
        c = Point(2*RIGHT)
        bc = always_redraw(lambda: Line(b, c))
        d = always_redraw(lambda: Point(
            midpoint(b.get_center(), c.get_center())))
        tancirc = always_redraw(
            lambda: tangent_circle(bc, d.get_center(), color=MONOKAI_PINK))
        line = Line(c, c.get_center() + 3*LEFT, color=MONOKAI_YELLOW)
        dots = self.circle_line_intersection(circle, line)
        a, e = dots
        # line = Line()
        # self.play(Create(Dot(c)))
        # self.play(Create(circle))
        self.add(d)
        self.play(Create(bc))
        self.play(Create(tancirc))
        self.play(b.animate.shift(LEFT))
        # print(type(dots[0]))
        # self.play(*(Create(Dot(d)) for d in dots))
        # self.play(Create(Line(*dots)))
        self.wait(2)
