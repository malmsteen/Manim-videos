from manim import *

import regex as re
import numpy as np
import string
from sympy import symbols
from sympy.solvers.solveset import nonlinsolve

MONOKAI_YELLOW = '#E6DB96'


class introInequality(Scene):
    def construct(self):
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        """)

        text = ['Дополнительные',
                'вступительные испытания МГУ', '2022, 6 поток']
        # title1 = Text('Дополнительные', font='sans serif')
        # title2 = Text('вступительные испытания МГУ', font='sans serif')
        title = Group(*[Text(t, font='sans serif', font_size=36)
                        for t in text]).arrange(DOWN)
        for t in title:
            t.to_edge(RIGHT)

        subtitle = Text('Неравенство', font='sans serif',
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
            fill_color=['#344C11', '#778D45'], sheen_direction=UP)\
            .set_y(logo.get_y())\
            .to_edge(RIGHT)\
            .shift(shift*LEFT)
        bgrect = BackgroundRectangle(logo, color=MONOKAI_ORANGE)

        self.play(FadeIn(title))
        self.play(
            subtitle.animate.shift(LEFT*(subtitle.width+1)),
            rect.animate.shift(RIGHT*shift),
            FadeIn(logo, shift=DOWN),
            run_time=3
        )
        self.wait(4)

        logosmall = logo.copy().scale(.4).to_corner(DR, buff=.2)
        self.play(ReplacementTransform(
            logo, logosmall))

        self.play(
            LaggedStart(
                rect.animate.shift(shift*LEFT),
                FadeOut(Group(title, subtitle)),
                lag_ratio=.1,
                run_time=2
            )
        )
        self.wait(.55)


class introPlane(Scene):
    def construct(self):
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        """)

        text = ['Дополнительные',
                'вступительные испытания МГУ', '2022, 6 поток']
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
            fill_color=['#344C11', '#778D45'], sheen_direction=UP)\
            .set_y(logo.get_y())\
            .to_edge(RIGHT)\
            .shift(shift*LEFT)
        bgrect = BackgroundRectangle(logo, color=MONOKAI_ORANGE)

        self.wait(1.3)
        self.play(FadeIn(title))
        self.wait()
        self.play(
            subtitle.animate.shift(LEFT*(subtitle.width+1)),
            rect.animate.shift(RIGHT*shift),
            FadeIn(logo, shift=DOWN),
            run_time=3
        )
        self.wait()

        logosmall = logo.copy().scale(.4).to_corner(DR, buff=.2)
        self.play(ReplacementTransform(
            logo, logosmall))

        self.play(
            LaggedStart(
                rect.animate.shift(shift*LEFT),
                FadeOut(Group(title, subtitle)),
                lag_ratio=.1,
                run_time=2
            )
        )


class planimetry(Scene):
    def tangent_circle(self, line, point, radius=1, d_alpha=1e-6, **kwargs):
        # circle tangent to line at point
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

        logo = Text('repetit-fm.ru', font='ubuntu')\
            .to_corner(DR, buff=.6).shift(.2*LEFT)\
            .copy().scale(.4).to_corner(DR, buff=.2)
        self.add(logo)

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
        conds = ['BD = CD', 'AF = 3 BF', 'AE=2CE', r'ED=\sqrt{10}', 'BC=?']
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
        # vertices = [v if type(v) != Dot else v.get_center()
        #             for v in [a, b, c, d, e, f]]
        sqrt = MathTex(r'\sqrt{10}', color=MONOKAI_BLUE)
        sqrt.add_updater(lambda m: m.next_to(mymidpoint(d, e), LEFT, buff=.1))
        vertices = [a, b, c, d, e, f]
        for v in vertices:
            print(type(v), '\n')
        tos = [DL, UR, DR, RIGHT, DOWN, LEFT]

        letters = []
        for l, v, to in zip(string.ascii_uppercase, vertices, tos):
            def func(m, v=v, to=to):
                return m.next_to(v, to, buff=.1)
            letters.append(MathTex(l).add_updater(func))
        self.play(
            LaggedStart(
                *(Write(l) for l in letters),
                Write(sqrt),
                lag_ratio=.3,
                run_time=1.5
            )
        )

        self.wait(11)

        middles = [(b, d), (c, d), (b, f), (f, a), (c, e), (a, e)]
        marks = ['a', 'a', 'x', '3x', 'y', '2y']
        mark_tos = [RIGHT, RIGHT, UL, UL, DOWN, DOWN]
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

        soln = [r'a^2 = BF \cdot AB', r'a^2 = x \cdot 4x',
                r',\, a=2x', r',\, x = \frac{a}{2},', r'\, AB = 2a']
        soln1 = [r'a^2 = y \cdot 3y',
                 r',\, y =\frac{a}{\sqrt3},', r'\, AC = a\sqrt3']
        soln2 = [r'\cos C = \frac{\frac{AC}{2}}{BC} ',
                 r' = \frac{\frac{a \sqrt3}{2}}{2a}', r'= \frac{\sqrt3}{4}']
        soln3 = [r'ED^2 = EC^2 + CD^2 - 2CE\cdot CD\cdot \cos C',
                 r'10 = \frac{a^2}{3} + a^2 - 2\cdot\frac{a}{\sqrt3}\cdot a \cdot \frac{\sqrt3}{4}',
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

        self.wait(10)
        self.clear()
        self.wait(2)


class param(Scene):
    def make_hint(self, mob, color=YELLOW):
        h = mob.height
        w = mob.width
        bg = RoundedRectangle(
            width=w+2.2,
            height=h + .2,
            color=GRAY,
            stroke_width=0,
            fill_opacity=.3,
            corner_radius=.1
        ).shift(LEFT)
        content = Group(mob, bg).to_corner(DL, buff=0).shift(LEFT*(3+w)+.5*UP)
        vline = Rectangle(width=.1,
                          height=bg.height,
                          stroke_width=0,
                          fill_color=color,
                          fill_opacity=1)\
            .to_corner(DL, buff=0)\
            .set_y(content.get_y())\
            .shift(2*DOWN)
        self.play(
            LaggedStart(
                vline.animate.shift(2*UP),
                content.animate.shift(RIGHT*(1.5+w)),
                lag_ratio=.8,
                run_time=1.5
            )
        )
        return (vline, content)

    def remove_hint(self, hint):
        vline, content = hint
        self.play(
            LaggedStart(
                AnimationGroup(
                    vline.animate.shift(2*DOWN),
                    content.animate.shift(LEFT*content.width),
                    lag_ratio=.9),
                # geomgroup.animate.shift(RIGHT*2),
                run_time=1,
                lag_ratio=.8
            ))

    def construct(self):
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        \DeclareMathOperator{\tg}{\mathop{tg}}
        """)
        MathTex.set_default(tex_template=tmpl, font_size=28)
        Dot.set_default(fill_opacity=0)
        problem = Tex(r'Найдите все значения параметра $a$ из интервала $(0,1)$, при которых для каждого $x$ из интервала $(0, \pi / 4)$ существует не более одного значения $y$ в интервале $(0, \pi / 4)$, такого что', tex_environment='flushleft')

        h0 = r'\tg(\alpha - \beta) = \frac{\tg \alpha - \tg \beta}{1 + \tg \alpha \tg \beta}'
        h1 = r"""\sin \alpha \sin \beta= \frac12 (\cos(\alpha - \beta) -\cos(\alpha + \beta)) \\
                 \cos\alpha \cos \beta = \frac12(\cos (x+y) + \cos(x-y)) """
        h2 = r'\cos \alpha - \cos \beta = -2\sin \frac{\alpha + \beta}{2} \cos \frac{\alpha - \beta}{2}'
        soln = [[r'\frac{\tg x \tg y}{\tg(a(x+y))}=', r'{ \tg(x+y)-\tg(a(x+y))    \over 1+\tg(x+y) \tg(a(x+y)) }'],
                [r' \tg x \tg y \over \tg(a(x+y))=',
                 r' \tg(x+y  - a(x+y))'],
                [r'\tg x \tg y = \tg((x+y)(1-a)) \tg(a(x+y))'],
                [r' \frac{\cos(x - y) - \cos(x+y)}{\cos(x+y) + \cos (x-y)} = \frac{\cos(x+y -2a(x+y)) - \cos (x+y)}{\cos (x+y) + \cos (x+y -2a(x+y))}'],
                [r' \frac{p - q}{p+q} = \frac{r - q}{q+r} '],
                [r' pq - q^2 + pr - qr = pr -pq + qr -q^2 '],
                [r' 2pq = 2 qr '],
                [r' q(p-r) = 0 '],
                [r' \cos(x-y) - \cos(x+y - 2a(x+y)) = 0 '],
                [r' 2 \sin (x - a(x+y)) \sin(y - a(x+y)) = 0 '],
                [r' x - a(x+y)=0, y - a(x+y) = 0 '],
                [r' y = \frac{1-a}{a} x, y = \frac{a}{1-a} x '],
                ]

        # text.to_edge(UP)
        problem = self.make_hint(problem)
        primo = MathTex(*soln[0]).to_edge(UP)
        segundo = MathTex(*soln[1])
        self.play(Write(primo))
        self.wait(2)
        self.remove_hint(problem)
        self.wait()
        alphabeta = self.make_hint(MathTex(h0))
        self.wait(3)
        self.play(Transform(primo[1:], segundo[1:].next_to(
            primo[0], RIGHT, buff=.2)))
        self.wait(3)
        self.remove_hint(alphabeta)

        g = Group(*(
            MathTex(*s) for s in soln[2:9])
        )\
            .arrange(DOWN)\
            .next_to(primo, DOWN)

        self.play(Write(g[0]))

        sinsin = self.make_hint(MathTex(h1))
        for s in g:
            self.play(Write(s))
            self.wait()

        # axes = Axes(
        #     x_range=[-1, 5],
        #     y_range=[-1, 5],
        #     x_length=3,
        #     y_length=3,
        #     tips=False,
        #     axis_config={"include_ticks": False}
        # )
        # axes_labels = axes.get_axis_labels()

        # one = axes.c2p(4, 4)
        # d_lines = axes.get_lines_to_point(one, color=MONOKAI_BLUE)
        # pi4x = MathTex(r'\frac{\pi}{4}', color=MONOKAI_BLUE).next_to(
        #     axes.c2p(4, 0), DOWN, buff=.3)
        # pi4y = MathTex(r'\frac{\pi}{4}', color=MONOKAI_BLUE).next_to(
        #     axes.c2p(0, 4), LEFT, buff=.3)

        # line1 = axes.plot(
        #     lambda x: 3*x, x_range=[-.5/3, 5.5/3], color=MONOKAI_PINK)
        # line2 = axes.plot(lambda x: 1/3 * x,
        #                   x_range=[-.5, 5.5], color=MONOKAI_PINK)

        # p = ValueTracker(0)
        # vert_line = always_redraw(
        #     lambda: DashedLine(
        #         axes.c2p(p.get_value(), 0),
        #         axes.c2p(p.get_value(), 4)
        #     )
        # )

        # self.play(Create(axes))
        # self.play(Write(axes_labels))
        # self.play(Create(d_lines, reverse=True))
        # self.play(FadeIn(pi4x), FadeIn(pi4y))
        # self.play(Create(line1))
        # self.play(Create(line2))
        # self.play(Create(vert_line))
        # self.play(p.animate.set_value(4/3), run_time=2)
        self.wait(3)


class inequality(Scene):
    def make_hint(self, mob, color=YELLOW, height=0, **kwargs):
        # heigth is position over bottom of frame
        h = mob.height
        w = kwargs.get('width', mob.width)
        bg = RoundedRectangle(
            width=w+2.2,
            height=h + .2,
            color=GRAY,
            stroke_width=0,
            fill_opacity=.3,
            corner_radius=.08
        ).shift(LEFT)
        content = Group(mob, bg).to_corner(
            DL, buff=0).shift(LEFT*(3+w)+.5*UP + UP*height)
        vline = Rectangle(width=.1,
                          height=bg.height,
                          stroke_width=0,
                          fill_color=color,
                          fill_opacity=1)
        vline.to_corner(DL, buff=0)\
            .set_y(content.get_y())\
            .shift(DOWN*3)
        self.play(
            LaggedStart(
                vline.animate.shift(UP*3),
                content.animate.shift(RIGHT*(1.5+w)),
                lag_ratio=.5,
                run_time=1.5
            )
        )
        return (vline, content)

    def remove_hint(self, hint):
        vline, content = hint
        self.play(
            LaggedStart(
                vline.animate.shift(2*DOWN),
                content.animate.shift(LEFT*content.width),
                lag_ratio=.4,
                run_time=1
            ))

    def make_shade(self, p1, p2):
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
        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        \DeclareMathOperator{\tg}{\mathop{tg}}
        \usepackage{amssymb}""")
        MathTex.set_default(tex_template=tmpl, font_size=28)

        logo = Text('repetit-fm.ru', font='ubuntu')\
            .scale(.4).to_corner(DR, buff=.2)
        self.add(logo)

        mainlog = r'\log _{x}\left(x^{2}+\frac{3}{2}\right)'
        ineq = MathTex(
            f'{mainlog} \\leqslant 4 \\log_{{x^2 + \\frac32}} (x)').to_edge(UP).shift(RIGHT)
        self.play(Write(ineq))
        self.wait(8)

        hint0 = self.make_hint(MathTex(r'\log_a b = {1 \over \log_b a}'))

        sub = f't = {mainlog}'
        ineq1 = [f't={mainlog},\, ',
                 r't \leqslant \frac4t,\,',
                 '{t^2 - 4 \over t} \leqslant 0', ]
        ineq1 = Group(*[MathTex(t) for t in ineq1]
                      ).arrange(RIGHT).next_to(ineq, DOWN)
        self.wait(3)
        self.play(Write(ineq1[0]))
        self.wait()
        self.play(Write(ineq1[1]))
        self.play(Write(ineq1[2]))

        self.remove_hint(hint0)

        numline = NumberLine(
            x_range=[-4, 4],
            length=5,
            include_ticks=False,
            color=MONOKAI_YELLOW,
            z_index=2).next_to(ineq1, DOWN, buff=.7)
        signs = ['-', '+', '-', '+']
        nums = [-2, 0, 2]
        colors = [MONOKAI_YELLOW, BLACK, MONOKAI_YELLOW]
        circles = [Circle(
            radius=.06,
            color=MONOKAI_YELLOW,
            fill_opacity=1,
            fill_color=col,
            stroke_width=2,
            z_index=3
        ).move_to(numline.n2p(n)) for n, col in zip(nums, colors)]
        roots = [-4, *nums, 4]
        pairs = zip(signs, roots[:-1], roots[1:])
        shown_signs = [MathTex(s, color=MONOKAI_YELLOW).move_to(midpoint(numline.n2p(p1), numline.n2p(p2))+UP*.3)
                       for s, p1, p2 in pairs]
        labels = [MathTex(n, color=MONOKAI_YELLOW).next_to(
            numline.n2p(n), DOWN) for n in nums]

        self.play(Create(numline))

        shades = self.make_shade(numline.n2p(-4), numline.n2p(-2)) +\
            self.make_shade(numline.n2p(0), numline.n2p(2))

        self.play(
            LaggedStart(
                *(Create(c) for c in circles),
                lag_ratio=.2,
            ),
            LaggedStart(
                *(FadeIn(l) for l in labels),
                lag_ratio=.2
            )
        )
        self.play(
            LaggedStart(
                *(FadeIn(s, shift=UP) for s in shown_signs),
                lag_ratio=.3,
                run_time=1))
        self.play(
            LaggedStart(
                *[Create(s) for s in shades],
                lag_ratio=.3,
                run_time=1
            )
        )

        ans = MathTex(
            r' t \in (-\infty;-2] \cup (0; 2] ').next_to(numline, DOWN, buff=.75)
        # self.play(Write(ans))
        self.wait(6)

        # case2 = [rf"""
        #         \left\{{
        #             \begin{{array}}{{l}}
        #             {mainlog} >  \\
        #             {mainlog} \leqslant
        #             \end{{array}}
        #         \right.
        #         """,
        #          r'\Leftrightarrow'
        #          r"""
        #         \left\{
        #             \begin{array}{l}
        #                 (x-1)\left(x^2 + \frac32 - 1 \right) > 0 \\
        #                 (x-1)\left(x^2 + \frac32 - x^2 \right) \leqslant 0
        #             \end{array}
        #             \right.
        #         """,
        #          '\Leftrightarrow',
        #          r"""
        #         \left\{
        #             \begin{array}{l}
        #                 x-1 > 0 \\
        #                 x-1 \leqslant 0
        #             \end{array}
        #         """,
        #          r'\Leftrightarrow x \in \varnothing']
        # case2 = Group(*[MathTex(c) for c in case2]
        #               ).arrange(DOWN).next_to(numline, DOWN)

        # system on x, rationalization and animation
        log1 = MathTex(f'{mainlog}')
        gt = MathTex('>')
        leq = MathTex(r'\leqslant')
        zero = MathTex('0')
        two = MathTex('2')
        g1 = Group(log1, gt, zero).arrange(
            RIGHT, buff=.15).next_to(numline, DOWN, buff=.7).shift(LEFT*1.5)
        log2 = log1.copy().shift(DOWN)
        g2 = Group(log2, leq, two) .arrange(
            RIGHT, buff=.15).next_to(g1, DOWN)
        brace = BraceBetweenPoints(
            log1.get_top(), log2.get_bottom(), direction=LEFT).shift(LEFT*.7)
        logx1 = MathTex(r'\log_x 1').next_to(gt, RIGHT, buff=.15)
        logxx = MathTex(r'\log_x x').next_to(leq, RIGHT, buff=.15)

        self.play(GrowFromCenter(brace),
                  *(Write(f) for f in g1),
                  *(Write(f) for f in g2))

        self.wait(7)
        ineq1 = log1[0][5:-1]
        self.play(Indicate(ineq1, color=MONOKAI_GREEN), run_time=2)
        self.wait(19)
        ineq2 = log2[0][5:-1]
        self.play(Indicate(ineq2, color=MONOKAI_GREEN), run_time=2)
        # 4 seconds on previous animations
        self.wait(22)

        self.play(FadeOut(zero), FadeIn(logx1))
        self.play(FadeIn(logxx), two.animate.scale(.7).next_to(
            logxx, UR, buff=0.01).shift(.08*DOWN))
        minus = MathTex('-').move_to(gt)
        self.wait(7)

        h1 = MathTex(
            r"""
            \log_a f > \log_a g
            \Leftrightarrow
            \left[
            \begin{array}{l}
                \left\{
                \begin{array}{l}
                    a > 1\\
                    f > g
                \end{array} \right.
                \\
                \left\{
                    \begin{array}{l}
                    a < 1\\
                    f < g
                    \end{array}
                \right.
            \end{array}
            \right.
            """)
        h2 = MathTex(
            r'\text{знак}(\log_a f - \log_a g) = \text{знак} ((a-1)(f-g))')
        hint1 = self.make_hint(h1, width=h1.width + 1.9)
        self.wait(8)
        hint2 = self.make_hint(
            h2, height=hint1[1].height + SMALL_BUFF)
        m = re.search('.*?(?=\=)', hint2[1][0].get_tex_string())
        signs = hint2[1][0][0]
        print(m.start(), m.end(), signs, '\n', hint2[1][0].get_tex_string())
        self.wait(2)
        self.play(Indicate(signs[:17]),
                  color=MONOKAI_GREEN, run_time=2)
        self.wait()
        self.play(Indicate(signs[18:]),
                  color=MONOKAI_GREEN, run_time=2)

        systems = hint1[1][0][0]
        self.wait(12)
        self.play(Indicate(systems[16:], color=MONOKAI_GREEN), run_time=3)

        self.wait(3)
        self.play(FadeIn(minus),
                  gt.animate.next_to(logx1, RIGHT, buff=.15),
                  FadeIn(MathTex('0').next_to(gt, RIGHT, buff=1.3)),
                  FadeIn(minus.copy().move_to(leq)),
                  leq.animate.next_to(logxx, RIGHT, buff=.15),
                  FadeIn(MathTex('0').next_to(leq, RIGHT, buff=1.3)),
                  run_time=3
                  )

        paran1 = MathTex(r'({{x-1}}){{\left(x^2 + \frac32 -1\right)}}{{> 0}}')
        paran2 = MathTex(
            r'({{x-1}}){{\left(x^2 + \frac32 - x^2\right)}}{{\leqslant 0}}')
        paran1.next_to(gt, RIGHT, buff=1.5)
        paran2.next_to(leq, RIGHT, buff=1.5)
        brace2 = brace.copy().next_to(paran1, LEFT, buff=0).set_y(brace.get_y())

        self.play(GrowFromCenter(brace2), Write(paran1), Write(paran2))

        self.play(
            LaggedStart(
                LaggedStart(
                    hint1[0].animate.shift(3*DOWN),
                    hint1[1].animate.shift(LEFT*hint1[1].width),
                    lag_ratio=.3
                ),
                LaggedStart(
                    hint2[0].animate.shift(4*DOWN),
                    hint2[1].animate.shift(LEFT*hint2[1].width),
                    lag_ratio=.3
                ),
            )
        )

        self.wait()
        self.play(Indicate(paran1[3], color=MONOKAI_GREEN),
                  Indicate(paran2[3], color=MONOKAI_GREEN),
                  run_time=3)
        self.wait(3)
        self.play(
            TransformMatchingTex(
                paran1, MathTex(
                    '{{x-1}}{{> 0}}').next_to(gt, RIGHT, buff=1.5)
            ),
            TransformMatchingTex(
                paran2, MathTex(
                    r'{{x-1}}{{\leqslant 0}}').next_to(leq, RIGHT, buff=1.5)
            ))
        self.wait(9)
        self.remove(logo)
        left_column = Group(*self.mobjects)
        self.add(logo)
        print(type(self.mobjects))
        # left_column -= logo
        self.play(left_column.animate.shift(5*LEFT))

        begincase1 = MathTex(
            *[f'{mainlog}', '\\leqslant', '-2', r'\log_x x'])
        case1 = [r'(x-1)\left( x^2 + \frac32 - \frac{1}{x^2} \right) \leqslant 0',
                 r'\frac{(x-1)(2x^4+3x^2 -2)}{x^2}  \leqslant 0',
                 r'\frac{(x-1)(2x^2 -1)(x^2+2)}{x^2} \leqslant 0']
        case1 = [MathTex(c) for c in case1]
        begincase1[0:2].to_edge(UP).shift(3*RIGHT)
        minusTwo = begincase1[2].next_to(begincase1[1], RIGHT, buff=.1)
        logx = begincase1[3].next_to(begincase1[1], RIGHT, buff=.1)
        minus = MathTex('-'). next_to(logx, LEFT, buff=.1)
        zero = MathTex('{{\\leqslant}} 0').next_to(logx, RIGHT, buff=.3)

        self.play(Write(begincase1[:3]))
        self.wait()
        self.play(FadeIn(logx), minusTwo.animate.scale(.7).next_to(
            logx, UR, buff=0).shift(.05*DOWN))
        self.wait()

        self.play(begincase1[1].animate.move_to(
            zero[0].get_center()), FadeIn(minus), FadeIn(zero[1]))

        left_column.add(minus, zero)

        g1 = Group(*case1)\
            .arrange(DOWN)\
            .next_to(begincase1, DOWN)

        self.wait(3)
        waits = [4, 2, 1]
        for c, w in zip(g1, waits):
            self.play(Write(c))
            self.wait(w)

        numline = NumberLine(
            x_range=[-4, 4],
            length=5,
            include_ticks=False,
            color=MONOKAI_YELLOW,
            z_index=2).next_to(g1, DOWN, buff=1)
        signs = ['-', '+', '+', '-', '+']
        nums = [-2.5, -1, 1, 2.5]
        colors = [MONOKAI_YELLOW, BLACK, MONOKAI_YELLOW, MONOKAI_YELLOW]
        circles = [Circle(radius=.06,
                          color=YELLOW_A,
                          fill_opacity=1,
                          fill_color=col,
                          stroke_width=1.5,
                          z_index=3)
                   .move_to(
            numline.n2p(n)) for n, col in zip(nums, colors)]
        points = [-4, *nums, 4]
        plus_h = MathTex('+').height
        minus_shifts = [0 if s == '+' else plus_h/2 for s in signs]
        pairs = zip(signs, points[: -1], points[1:])
        shown_signs = [MathTex(s, color=MONOKAI_YELLOW).move_to(midpoint(numline.n2p(p1), numline.n2p(p2))+UP*.3)
                       for s, p1, p2 in pairs]

        texnums = [r'-\frac{1}{\sqrt2}', '0', r'\frac{1}{\sqrt2}', '1']
        labels = [MathTex(texnum, color=MONOKAI_YELLOW).next_to(numline.n2p(n), DOWN)
                  for n, texnum in zip(nums, texnums)]

        self.wait(3)
        self.play(Create(numline))
        shades = self.make_shade(numline.get_start(), numline.n2p(-2.5)) +\
            self.make_shade(numline.n2p(1), numline.n2p(2.5))

        self.play(
            LaggedStart(
                *(Create(c) for c in circles),
                lag_ratio=.2,
            ),
            LaggedStart(
                *(FadeIn(l) for l in labels),
                lag_ratio=.2,
            ),
            run_time=1
        )
        self.wait()
        self.play(
            LaggedStart(
                *(FadeIn(s, shift=UP) for s in shown_signs),
                lag_ratio=.3,
                run_time=1))
        self.play(
            LaggedStart(
                *[Create(s) for s in shades],
                lag_ratio=.3,
                run_time=1
            )
        )
        self.wait(2)

        final_ans = MathTex(r"\left[ \frac{1}{\sqrt2}; 1 \right)")
        # fital_ans = MathTex(r'\left[ \right)')
        final_ans.next_to(numline, DOWN, buff=1.5)
        self.play(Write(final_ans))
        self.wait()
        self.play(final_ans.animate.scale(1.7).set_color(MONOKAI_GREEN))
        self.wait(15)


class test(Scene):
    def construct(self):
        two = MathTex(r'{{\leqslant}}{{2}}')
        log = MathTex(r'{{\leqslant}}\log_x x^{{2}}')

        self.play(TransformMatchingTex(two, log))
        self.wait(3)
