from manim import *


class Example(Scene):
    def construct(self):
        base = Square(color=ORANGE)
        target = Circle(color=GREEN)
        line = Line(3*LEFT, 3*RIGHT, buff=1, color=RED)\
            .next_to(base, DOWN, buff=1)
        up_square = Square(fill_color=PINK, fill_opacity=0)\
            .scale(5).next_to(line, UP, buff=0).set_opacity(0)
        down_square = Square(fill_color=BLUE, fill_opacity=0)\
            .scale(5).next_to(line, DOWN, buff=0).set_opacity(0)
        slider = VGroup(up_square, down_square, line)

        self.add(slider)

        def get_intersection_updater(no_added_mob, background):
            def updater(added_mob):
                added_mob.become(Intersection(
                    no_added_mob, background).match_style(no_added_mob))
            return updater

        pre_mob = VMobject().add_updater(get_intersection_updater(base, up_square))
        pos_mob = VMobject().add_updater(get_intersection_updater(target, down_square))
        self.add(pre_mob, pos_mob)

        # self.play(Write(MathTex('\int_0^1 f(x) dx')))
        self.play(slider.animate.shift(UP*4), run_time=4)
        self.wait(3)
