from manim import *
import numpy as np

SCALE_FACTOR = 1
tmp = config.pixel_height
config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
config.frame_height = config.frame_height / SCALE_FACTOR
config.frame_width = config.frame_height * 9 / 16
FRAME_HEIGHT = config.frame_height
FRAME_WIDTH = config.frame_width


class AnimatedFunction(Scene):
    def setup(self, add_border=True):
        if add_border:
            self.border = Rectangle(
                width=FRAME_WIDTH,
                height=FRAME_HEIGHT,
                color=WHITE
            )
            self.add(self.border)

    def construct(self):

        formula = MathTex(
            r"y = x^{\frac23} + 1.1 \sin a x * \sqrt{4-x ^2}",
            substrings_to_isolate=["x", "y", "a "])

        formula.set_color_by_tex_to_color_map(
            {"x": GREEN, "y": RED, "a ": BLUE})

        axes = Axes(
            x_range=[-2, 2, 0.1],
            y_range=[-3, 3.7, 0.1],
            x_length=5,
            axis_config={
                "color": BLUE,
                "include_ticks": False
            },
        ).scale(.7).shift(UP)
        axes_labels = axes.get_axis_labels()

        a_tracker = ValueTracker(0)

        def func(x):
            a = a_tracker.get_value()
            return np.cbrt(x)**2 + 1.1 * np.sin(a * .5 * x) * np.sqrt(4 - x**2)

        graph = always_redraw(lambda: axes.plot(
            func, color=RED, dt=0.05, stroke_width=1.5))
        graph.stroke_width = .3

        number = DecimalNumber(
            a_tracker.get_value(),
            color=BLUE,
            group_with_commas=False,
            num_decimal_places=0
        )


        number.add_updater(lambda m: m.set_value(a_tracker.get_value()))

        formula.next_to(axes, DOWN).scale(.6)
        a = MathTex("a = ", color=BLUE)
        # number.next_to(a, RIGHT)

        vg = VGroup(a, number).next_to(formula, DOWN).arrange(
            RIGHT).scale(.7).next_to(formula, DOWN)
        self.add(vg)

        self.add(axes, axes_labels, graph)

        self.play(Write(formula))

        self.play(
            a_tracker.animate.set_value(1700),
            run_time=58,
            rate_func=there_and_back
        )
        self.wait()
