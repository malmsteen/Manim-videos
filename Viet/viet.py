from manim import *
import numpy as np
import random
from itertools import cycle

SCALE_FACTOR = 1
tmp = config.pixel_height
config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
config.frame_height = config.frame_height / SCALE_FACTOR
config.frame_width = config.frame_height * 9 / 16
FRAME_HEIGHT = config.frame_height
FRAME_WIDTH = config.frame_width





class AnimatedFunction(Scene):

    def construct(self):
        logo = Text("Филипенко Евгений\nrepetit-fm.ru", color=GRAY, font_size=12).to_corner(DR).shift(DOWN*.2)

        eqn0 = MathTex(r'a x^2 + b x + c = 0', substrings_to_isolate= [ 'a','b','c', 'x']).to_edge(UP)
        eqn1 = MathTex(r'{{x_1}} + {{x_2}} = -{ {{b}} \over {{a}} }')
        eqn2 = MathTex(r'{{x_1}} \cdot {{x_2}} = { {{c}} \over {{a}} }')
        color_map = {'x^2': GREEN, 'x_1': GREEN, 'x_2':GREEN, 'x': GREEN, 'a':BLUE, 'b':BLUE, 'c':BLUE, 'cdot': WHITE, 'p':GREEN, 'q':GREEN}
        
        g1 = VGroup(eqn1, eqn2).arrange(DOWN, aligned_edge = LEFT).shift(2*UP)
        brace1 = Brace(g1, LEFT)
        # brace = MathTex(r"\{").match_height(g1)
        # brace.move_to(g1, LEFT)
        g1.add(brace1)
        
        eqn3 = MathTex(r"{{a}} {{x_1}} + {{a}} {{x_2}} = -b", substrings_to_isolate=['x_1', 'x_2', 'a', 'b'])
        eqn4 = MathTex(r"{{a}} {{x_1}} \cdot {{a}} {{x_2}} = a c", substrings_to_isolate=['x_1', 'x_2', 'a', 'cdot' 'c'])

        eqn5 = MathTex(r'5 x^2 - 13 x + 6 = 0', substrings_to_isolate= [ '5','6','13', '0', 'x'])
        digits_dict = {str(i): BLUE for i in range(100) if i != 2}
        ax1 = [eqn3[:3], eqn4[:3]]
        
        
        
        print(type(ax1[0]))
        ax2 = [eqn3[4:7], eqn4[4:7]]
        

        for f in [eqn0, eqn1, eqn2, eqn3, eqn4, eqn5]:
            f.set_color_by_tex_to_color_map({**color_map})
        eqn5.set_color_by_tex_to_color_map({**digits_dict, **color_map})

        g2 = VGroup(eqn3, eqn4).arrange(DOWN, aligned_edge=LEFT)        
        brace2 = Brace(g2, LEFT)
        g3 = g2.add(brace2)
        VGroup(g1, g2).arrange(DOWN, aligned_edge=LEFT)
        
        # system2.next_to(system1, DOWN)
        
        p = [MathTex('p', color=RED).move_to(ax.get_center()) for ax in ax1]
        q = [MathTex('q', color=RED).move_to(ax.get_center()) for ax in ax2]
        sur_rect = lambda vg: Rectangle(
            height = np.linalg.norm(vg.get_top() - vg.get_bottom()) + SMALL_BUFF,
            width = np.linalg.norm(vg.get_left() - vg.get_right()) + SMALL_BUFF, 
            color=YELLOW
            ).move_to(vg.get_center())
        
        # rects1, rects2 = [[SurroundingRectangle(r) for r in (x,y)] for x, y in zip(ax1, ax2)]
        vg = ax1[0]
        print(vg.height)
        rect = Rectangle(height = 1, width = 2).move_to(vg.get_center())
        rects1 = [sur_rect(r) for r in [ax1[0], ax2[0]]]
        rects2 = [sur_rect(r) for r in [ax1[1], ax2[1]]]
        self.play(Write(eqn0), FadeIn(logo), run_time = 3)
        self.wait(8)
        self.play(Write(g1), run_time = 6)
        self.wait(8)
        self.play(Write(g3), run_time = 3)
        self.wait(6)
        self.play(LaggedStart(
            AnimationGroup( [ShowPassingFlash(r, time_width = .5) for r in rects1]),
            AnimationGroup( [ShowPassingFlash(r, time_width = .5) for r in rects2]),
            lag_ratio = 2,
            run_time = 2
        ))
        # self.play(FadeIn(Line(start=ax1[0].get_bottom(), end = ax1[0].get_top())))
        # self.play(FadeIn(Line(start=ax1[0].get_left(), end = ax1[0].get_right()))) 
        # self.play(FadeIn(sur_rect(g2)))
        # self.play(ShowPassingFlash(rect))
        self.wait()
        self.play(FadeOut(*ax1, *ax2), FadeIn(*p, *q), run_time = 3)
        self.wait(5)
        

        g4 = VGroup(*eqn3)
        g5 = VGroup(*eqn4)
        
        # g6 = VGroup(*eqn)
        # g2.remove(g2[0][2])
        g4.remove(*[g4[i] for i in [0,1,2,4,5,6]])
        g5.remove(*[g5[i] for i in [0,1,2,4,5,6]])
        gg = VGroup(g4, g5)
        # eqn3 = [eqn3[3:4],eqn3[7:]]
        # g2.add(*eqn3)
        gg.add(p,q, brace2)
        self.wait(2)
        # system2.add(p,q)
        self.play(LaggedStart(
            FadeOut(eqn0, g1),
            gg.animate.shift(3*UP),
            # g4.animate.to_edge(UP),
            # g5.animate.to_edge(UP)
            ),
                lag_ratio = 1)
        eqn5.next_to(gg, DOWN, buff=1)
        
        self.play(Write(eqn5))
        self.wait(15)

        ans1 = MathTex("{{x_1}} = { {{10}} \over {{5}} }")
        ans2 = MathTex("{{x_2}} = { {{3}} \over {{5}} }")
        color_map = {"x_1": GREEN, "x_2": GREEN, "10": RED, "3": RED, "5": BLUE}
        ans = VGroup(ans1, ans2).arrange(RIGHT).next_to(eqn5, DOWN)
        ans1.set_color_by_tex_to_color_map(color_map)
        ans2.set_color_by_tex_to_color_map(color_map)

        self.play(Write(ans1[2]), Write(ans2[2]))
        self.wait(3)
        self.play(Write(ans1[3:]), Write(ans2[3:]), FadeIn(ans1[:2]), FadeIn(ans2[:2]))
        self.wait(15)
        # self.play(Write(ans1[:2]), Write(ans2[:2]))
        # self.wait()

        print(len(self.mobjects))
        
        to_fade = VGroup(ans1, ans2, gg, eqn5 )
        self.play(*[
            AnimationGroup(
                *(FadeOut(mobj, scale=.5) for mobj in self.mobjects), 
                lag_ratio=.1
            )
        ])
        self.wait()

        text = Text("Не совсем все ;)", font_size=28)
        end = Text("Теперь все", font_size=28)

        self.play(FadeIn(text))
        self.wait(12)
        self.play(FadeOut(text), FadeIn(end), run_time = 2)
        self.wait(2)
        self.play(FadeOut(end))
        self.wait(.5)















        



