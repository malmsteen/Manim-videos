
from manim import *
from local_colors import *
from typing import Callable, Iterable, Optional, Tuple, Type, Union

import numpy as np
SCALE_FACTOR = 1
tmp= config.pixel_height
config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
config.frame_height = config.frame_height / SCALE_FACTOR
config.frame_width = config.frame_height * 9 /16
FRAME_HEIGHT = config.frame_height
FRAME_WIDTH = config.frame_width

class Indicate_scale(Transform):
    """Indicate a Mobject by temporarily resizing and recoloring it.

    Parameters
    ----------
    mobject
        The mobject to indicate.
    scale_factor
        The factor by which the mobject will be temporally scaled
    color
        The color the mobject temporally takes.
    rate_func
        The function defining the animation progress at every point in time.
    kwargs
        Additional arguments to be passed to the :class:`~.Succession` constructor

    Examples
    --------
    .. manim:: UsingIndicate

        class UsingIndicate(Scene):
            def construct(self):
                tex = Tex("Indicate").scale(3)
                self.play(Indicate(tex))
                self.wait()
    """

    def __init__(
        self,
        mobject: Mobject,
        scale_factor: float = 1.2,
        rate_func: Callable[[float, Optional[float]], np.ndarray] = there_and_back,
        **kwargs
    ) -> None:
        self.color = color
        self.scale_factor = scale_factor
        super().__init__(mobject, rate_func=rate_func, **kwargs)

    def create_target(self) -> Mobject:
        target = self.mobject.copy()
        target.scale(self.scale_factor)
        return target



class TikTok(Scene):
    def setup(self, add_border = True):
        if add_border:
            self.border = Rectangle(
                width = FRAME_WIDTH,
                height = FRAME_HEIGHT,
                color = WHITE
            )
            self.add(self.border)
    def construct(self):

        tmpl = TexTemplate()
        tmpl.add_to_preamble(r"""
        \usepackage{mathtext}
        \usepackage[T2A]{fontenc}
        \usepackage[utf8]{inputenc}
        """)
        Tex.set_default(tex_template=tmpl, font_size=28)
        MathTex.set_default(tex_template=tmpl, font_size=28)

        text = Tex("Hello world", color = RED)
        perc1 = Tex(r"$15,5 \%$ от 49", color = MONOKAI_BLUE)
        perc2 = Tex(r"$49 \%$ от 15,5", color = MONOKAI_PURPLE)
        disjunc = MathTex(r"\lor")

        # text.to_edge(LEFT, buff=0).to_edge(DOWN, buff= 0)
        # self.play(Write(text))
        self.play(Write(perc1))
        self.play(perc1.animate.shift(LEFT))
        self.play(FadeIn(disjunc.next_to(perc1, RIGHT)))
        self.play(Write(perc2.next_to(disjunc, RIGHT)))
        self.wait(2)

        ans1 = MathTex(r"49 \cdot 0,155", color = MONOKAI_BLUE)
        ans2 = MathTex(r"15,5 \cdot 0,49", color = MONOKAI_PURPLE)
        eq = Tex('=')
        self.play(Write(ans1.next_to(perc1, DOWN)))
        self.play(Write(ans2.next_to(perc2, DOWN)))
        self.play(FadeIn(eq.next_to(disjunc, DOWN, buff = 0.35)))
        self.wait(2)

        g = VGroup(ans1, eq, ans2)
        self.play(Indicate_scale(g))
        self.wait(2)
