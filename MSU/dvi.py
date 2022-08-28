from turtle import down, right
from manim import *

import numpy as np
import string
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve


class intro(Scene):
    def construct(self):
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        """)

        text = ['Дополнительные',
                'вступительные испытания МГУ', '2022, 5 поток']
        # title1 = Text('Дополнительные', font='sans serif')
        # title2 = Text('вступительные испытания МГУ', font='sans serif')
        title = Group(*[Text(t, font='sans serif', font_size=36)
                        for t in text]).arrange(DOWN)
        for t in title:
            t.to_edge(RIGHT)

        subtitle = Text('Планиметрия', font='sans serif',
                        font_size=34, color=RED_A)
        logo = Text('repetit-fm.ru', font='ubuntu')

        g = Group(title, subtitle).arrange(DOWN, buff=1)
        title.to_edge(RIGHT).shift(UP)
        subtitle.to_edge(RIGHT).shift(RIGHT*(subtitle.width+1) + UP)
        logo.to_corner(DR, buff=.6).shift(.2*LEFT)

        shift = 14
        rect = RoundedRectangle(
            height=logo.height*1.2,
            width=15,
            stroke_width=0,
            fill_opacity=1,
            corner_radius=.1,
            fill_color=[GREEN, RED],
            sheen_direction=UP)\
            .set_y(logo.get_y())\
            .to_edge(RIGHT)\
            .shift(shift*LEFT)
        bgrect = BackgroundRectangle(logo, color=MONOKAI_ORANGE)

        self.play(FadeIn(title))
        self.wait()
        self.play(
            subtitle.animate.shift(LEFT*(subtitle.width+1)),
            rect.animate.shift(RIGHT*shift),
            FadeIn(logo, shift=DOWN),
            run_time=3
        )

        self.wait(2)
        logosmall = logo.copy().scale(.4).to_corner(DR, buff=.2)
        self.play(ReplacementTransform(
            logo, logosmall))

        self.play(
            LaggedStart(
                rect.animate.shift(shift*LEFT),
                FadeOut(Group(title, subtitle)),
                lag_ratio=.7,
                run_time=3
            )
        )


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

    def make_hint(self, vmob):
        h = vmob.height
        w = vmob.width
        bg = RoundedRectangle(
            width=w+2.2,
            height=h + .2,
            color=GRAY,
            stroke_width=0,
            fill_opacity=.3,
            corner_radius=.1
        ).shift(LEFT)
        vgroup = VGroup(vmob, bg).to_corner(DL, buff=0).shift(LEFT*(3+w)+.5*UP)
        ym = Rectangle(width=.1,
                       height=bg.height,
                       stroke_width=0,
                       fill_color=YELLOW,
                       fill_opacity=1)\
            .to_corner(DL, buff=0)\
            .set_y(vgroup.get_y())\
            .shift(2*DOWN)
        self.play(
            LaggedStart(
                ym.animate.shift(2*UP),
                vgroup.animate.shift(RIGHT*(1.5+w)),
                lag_ratio=.8,
                run_time=1.5
            )
        )

        return (ym, vgroup)

    def make_prime(self, p1, p2, **kwargs):
        vec = p2-p1
        len = .15
        lin = Line(p1, p2, **kwargs).scale(1/np.linalg.norm(vec)*len)
        lin.rotate(TAU/4)
        return lin

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
            r'Окружность, проходящая через вершину $A$ треугольника $A B C$, касается его стороны $B C$ в точке $D$ и пересекает стороны $A C$ и $A B$ в точках $E$ и $F$ соответственно. Известно, что $A F=3 B F$, $B D=C D, A E=2 C E$ и что $E D=\sqrt{10}$. Найдите $B C$.', tex_environment='flushleft')

        circle = Circle(radius=1, color=MONOKAI_PINK).shift(RIGHT)
        # bc = TangentLine(circle, alpha=.13, length=3, color=MONOKAI_BLUE)

        c = 4*RIGHT
        b = Dot(3.5*RIGHT + 3 * UP)
        a = c + 3 * LEFT
        cb = always_redraw(lambda: Line(c, b.get_center(),
                                        color=MONOKAI_BLUE, z_index=-1))
        # ab = always_redraw(lambda: Line(a, b), color=MONOKAI_BLUE)
        d = always_redraw(lambda: Dot(
            midpoint(b.get_center(), c)))
        tancirc = always_redraw(
            lambda: self.tangent_circle(cb, d.get_center(), color=MONOKAI_PINK))
        prime1 = always_redraw(lambda: self.make_prime(
            b.get_center(), d.get_center(), color=MONOKAI_BLUE))
        prime2 = always_redraw(lambda: self.make_prime(
            c, d.get_center(), color=MONOKAI_BLUE))
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

        dano = Tex('Дано:')
        conds = ['BD = CD', 'AF = 3 BF', 'AE=2CE', 'BC=?']
        given = VGroup(dano, *[MathTex(c) for c in conds])\
            .arrange(DOWN)\
            .next_to(abc, RIGHT)\
            .shift(UP+RIGHT)
        ym, h = self.make_hint(text)
        self.play(Create(abc))
        # self.play()
        self.add(cb, Dot(a), Dot(c), b, d, e, f)
        self.play(Create(tancirc), Create(prime1), Create(prime2))
        self.play(Create(de))
        self.wait()
        self.play(
            LaggedStart(
                *(FadeIn(giv, shift=UP) for giv in given),
                lag_ratio=.3,
                run_time=1.5
            ))
        vertices = [a, b, c, d, e, f]
        for v in vertices:
            print(type(v), '\n')
        # vertices = [v if type(v) != Dot else v.get_center()
        #             for v in [a, b, c, d, e, f]]
        tos = [DL, UR, DR, RIGHT, DOWN, LEFT]

        middles = [(b, d), (c, d), (b, f), (f, a), (c, e), (a, e)]
        marks = ['a', 'a', 'x', '3x', 'y', '2y']
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
            marksxy.append(
                MathTex(mark, color=MONOKAI_YELLOW).add_updater(func))

        self.wait(4)
        waits = [0, 2, 0, 1, 0, 0]
        for m, w in zip(marksxy, waits):
            self.play(Write(m))
            self.wait(w)

        # self.play(*(Write(m) for m in marksxy))
        # self.add(tancirc)
        letters[-2].clear_updaters()
        letters[-1].clear_updaters()

        # for mob in self.mobjects:
        #     mob.clear_updaters()
        geomgroup = Group(abc, *letters, *marksxy, tancirc, cb, de, ca, given)
        # geomgroup = Group(*self.mobjects)
        # geomgroup.remove(ym, h)

        self.play(
            LaggedStart(
                AnimationGroup(
                    ym.animate.shift(2*DOWN),
                    h.animate.shift(LEFT*h.width),
                    lag_ratio=.9),
                # geomgroup.animate.shift(RIGHT*2),
                run_time=1,
                lag_ratio=.8
            ))

        self.wait()
        # self.play(geomgroup.animate.shift(RIGHT))

        # group = Group(*[MathTex(s) for s in [soln3]])\
        #     .arrange(DOWN)\
        #     .to_corner(UL)
        # for s in group:
        #     s.to_edge(LEFT).shift(RIGHT)

        # group = Tex(r"""$BD^2 = AF \cdot BF$, $ a^2 = x \cdot 4x$,
        # $a = 2x$, $x = \frac{a}{2}$, $BC = 2a$

        # $a ^ 2 = y \cdot 3y$, $y =\frac{a}{\sqrt3}$, $AC = a\sqrt3$

        # $\cos C = \frac{\frac{AC}{2}}{BC} $,
        # $ = \frac{\frac{a \sqrt3}{2}}{2a}$, $= \frac{\sqrt3}{4}$

        # $ED ^ 2 = EC ^ 2 + CD ^ 2 - 2CE\cdot CD\cdot \cos C$

        # $10 = \frac{a ^ 2}{3} + a ^ 2 - 2\cdot\frac{a}{\sqrt3}\cdot \frac{\sqrt3}{4}$

        # $10 = a ^ 2 +\frac{a ^ 2}{3} - \frac{a ^ 2}{2}$,
        # $10 =\frac{5a ^ 2}{6}$,
        # $a = 2\sqrt3$,
        # $BC = 4\sqrt3$""")
        # self.play(Write(group))

        plan = Group(*[Tex(p) for p in
                       [r'$AB$ и $AC$ через $a$',
                        r'$\longrightarrow$',
                        r'$\cos C$',
                        r'$\longrightarrow$',
                        r'$a$',
                        r'$\longrightarrow$'
                        '$BC$']
                       ])
        plan.arrange(RIGHT).next_to(geomgroup, DOWN)

        self.wait(15)
        waits = [1, 1, 1, 6, 0, 1]
        for p, w in zip(plan, waits):
            self.play(Write(p))
            self.wait(w)

        soln = [r'a^2 = AF \cdot BF', r'a^2 = x \cdot 4x',
                r',\, a=2x', r',\, x = \frac{a}{2},', r'\, AB = 2a']
        soln1 = [r'a^2 = y \cdot 3y',
                 r',\, y =\frac{a}{\sqrt3},', r'\, AC = a\sqrt3']
        soln2 = [r'\cos C = \frac{\frac{AC}{2}}{BC} ',
                 r' = \frac{\frac{a \sqrt3}{2}}{2a}', r'= \frac{\sqrt3}{4}']
        soln3 = [r'ED^2 = EC^2 + CD^2 - 2CE\cdot CD\cdot \cos C',
                 r'10 = \frac{a^2}{3} + a^2 - 2\cdot\frac{a}{\sqrt3}\cdot \frac{\sqrt3}{4}',
                 r'10=a^2 +\frac{a^2}{3} - \frac{a^2}{2}',
                 r'10 =\frac{5a^2}{6}',
                 r',\, a = 2\sqrt3,',
                 r'\quad BC = 4\sqrt3']

        self.wait(2)
        g = MathTex(soln[0]).to_corner(UL)
        g1 = MathTex(*soln[1:]). next_to(g, DOWN).to_edge(LEFT)

        self.play(Write(g))
        self.wait(1)

        for s in g1:
            self.play(Write(s))
            self.wait()

        self.wait(3)
        waits = [1, 2, 1]
        g2 = MathTex(*soln1).next_to(g1, DOWN).to_edge(LEFT)
        for s in g2:
            self.play(Write(s))
            self.wait()

        self.play(Indicate(g1[-1]), Indicate(g2[-1]), run_time=3)
        self.wait(4)
        self.play(b.animate.set_x(ca.get_x()),
                  letters[-2].animate.next_to(eprime, DOWN, buff=.1),
                  letters[-1].animate.next_to(fprime, UL, buff=.1),
                  e.animate.become(Dot(eprime)),
                  f.animate.become(Dot(fprime)),
                  run_time=3)
        self.wait(5)
        dline = DashedLine(b, ca.get_center(), color=MONOKAI_BLUE)
        rightangle = DashedVMobject(
            RightAngle(dline, ca, quadrant=(-1, -1),
                       color=MONOKAI_BLUE, length=.2),
            num_dashes=9
        )
        anglec = Angle(cb, ca, radius=.3)

        g3 = MathTex(*soln2).next_to(g2, DOWN).to_edge(LEFT)
        self.play(Write(g3[0]), Create(dline))
        self.play(Create(rightangle))
        self.play(Create(anglec))
        self.wait(5)
        self.play(Write(g3[1:]))
        self.wait(2)

        g4 = MathTex(soln3[0]).next_to(g3, DOWN).to_edge(LEFT)
        self.play(Write(g4))

        g5 = MathTex(soln3[1]).next_to(g4, DOWN).to_edge(LEFT)
        self.play(Write(g5))

        self.wait()

        g6 = MathTex(soln3[2]).next_to(g5, DOWN).to_edge(LEFT)
        self.play(Write(g6))
        g7 = MathTex(*soln3[3:]).next_to(g6, DOWN).to_edge(LEFT)
        for s in g7:
            self.play(Write(s))

        self.play(Indicate(g7[-1], color=MONOKAI_GREEN), run_time=3)

        self.wait()


class param(Scene):
    def construct(self):
        pass
