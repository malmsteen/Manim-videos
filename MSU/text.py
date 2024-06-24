from manim import *
from turtle import down, right


class test(Scene):
    def construct(self):
        frac = MathTex(r'{ {{a}} \over {{b}} } {{=}} {{c}}')
        prod = MathTex('{{a}}  {{=}} {{c}} {{b}}')

        self.play(TransformMatchingTex(frac, prod))
        self.wait(2)
