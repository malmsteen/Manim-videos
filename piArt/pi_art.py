# symbol Visualization
# Numberphile Video: https://youtu.be/NPoj8lk9Fo4
# Martin Krzywinski and Cristian Ilies Vasile: http://mkweb.bcgsc.ca/pi/art/
#
#
# Working of the formation of this code to make this Visualization:
# Step 1: Every digit of pi is connected to its next digit. Bezier curves are used
# to connect the corresponding numbered arcs.
# For ex: pi = 3.141 So, the bezier curve starts from the 3rd arc and ends on 1st arc.
# Next curve would start from 1st arc and goes to 4th arc

from manim import *
from mpmath import mp
import numpy as np


# from https://stackoverflow.com/a/13316984


sol_base03=    ManimColor("#002b36")
sol_base02=    ManimColor("#073642")
sol_base01=    ManimColor("#586e75")
sol_base00=    ManimColor("#657b83")
sol_base0=     ManimColor("#839496")
sol_base1=     ManimColor("#93a1a1")
sol_base2=     ManimColor("#eee8d5")
sol_base3=     ManimColor("#fdf6e3")
sol_yellow=    ManimColor("#b58900")
sol_orange=    ManimColor("#cb4b16")
sol_red=       ManimColor("#dc322f")
sol_magenta=   ManimColor("#d33682")
sol_violet=    ManimColor("#6c71c4")
sol_blue=      ManimColor("#268bd2")
sol_cyan=      ManimColor("#2aa198")
sol_green=     ManimColor("#859900")

class PiCircle(Scene):
    def get_n_digits_of_symbol(n):
        mp.dps = n
        return [3] + [int(i) for i in list(str(mp.pi))[2:]]
    
    def setup(self):
        super().setup()
        self.colors = [DARK_BROWN, ORANGE, PURPLE, LIGHT_PINK,
                  TEAL, BLUE, BLUE_E, BLUE_B, GREEN_E, GREEN_B]
        self.num_of_arcs = 10  # obviously
        self.offset = 5 * DEGREES  # space b/w two arcs
        self.radius = 3
        self.arc_length = (TAU / self.num_of_arcs) - self.offset        
        self.n = 3150  # number of digits of pi used
        self.path_config = {
            'width':.7,
            'opacity':.2
            } # another combination is 1, 0.1
        
        self.symbol = MathTex("\\pi", font_size=72)

    def get_n_digits_of_symbol(self, n):
        mp.dps = n
        return [3] + [int(i) for i in list(str(mp.pi))[2:]]

    def get_arcs_point(self):
        return [
            (
                np.array([(self.radius + 0.3) * np.sin(s),
                        (self.radius + 0.3) * np.cos(s), 0]),
                np.array([(self.radius + 0.3) * np.sin(e),
                        (self.radius + 0.3) * np.cos(e), 0])
            )
            for s, e in zip(
                np.linspace(self.offset / 2, TAU - self.arc_length - self.offset / 2, self.num_of_arcs),
                np.linspace(self.arc_length + self.offset / 2, TAU - self.offset / 2, self.num_of_arcs)
            )
        ]
    
    def draw_sectors_and_symbol(self):
        
        symbol = self.symbol
        circle = VGroup() 
        circle.add(symbol)

        # position of numbers
        num_points = [
            np.array([(self.radius + 0.7) * np.sin(s),
                    (self.radius + 0.7) * np.cos(s), 0])
            for s in np.linspace(self.offset / 2 + self.arc_length / 2, TAU - self.arc_length / 2 - self.offset / 2, self.num_of_arcs)
        ]

        nums = VGroup(*[
            Tex(str(i), font_size=36) for i in range(self.num_of_arcs)
        ])

        for i, num in enumerate(nums):
            num.move_to(num_points[i])
        circle.add(nums)

        arcs_point = self.get_arcs_point()
        # arc's start and end points as a tuple
        arcs = VGroup(*[
            ArcBetweenPoints(
                p[0], p[1],
                color=self.colors[i],
                angle=-self.arc_length,
                stroke_width=20
            )
            for i, p in enumerate(arcs_point)
        ])
        circle.add(arcs)

        self.play(
            AnimationGroup(
                LaggedStart(
                *(Write(arc) for arc in arcs), lag_ratio = .3),
                LaggedStart(
                *(Write(num) for num in nums), lag_ratio = .3),
                lag_ratio=0.2
            ),
            run_time=5,
            rate_func=linear,
        )
        self.play(Write(symbol), run_time=2)

    def make_paths(self):
        
        # defining the start point of the bezier curves so they won't touch the arcs
        curve_points = [
            np.array([self.radius * np.sin(s), self.radius * np.cos(s), 0])
            for s in np.linspace(self.offset / 2, TAU - self.arc_length - self.offset / 2, self.num_of_arcs)
        ]

        # Step 2:
        # The position of the starting point of the bezier curve is same as the
        # position of the number in the digits of pi.
        # For ex: pi = 3.141
        # First curve starts from position one of 3rd arc and ends at position 2 of 1st arc.
        # Next curve starts from the point from previous curve ends and goes to 3rd position of
        # 4th arc.

        # I'm using SmallDot() or Dot() so that it is easily rotated to mark the position where the curve would end.
        curve_dots = [Dot(p) for p in curve_points]
        curve_dots1 = curve_dots.copy()
        curve_pointer = [0] * len(curve_dots)        

        symbol_n = self.get_n_digits_of_symbol(self.n)
        path = VGroup()  
        paths = VGroup()  # group of bezier curves
        len_of_arc = 360 / self.num_of_arcs - self.offset / DEGREES # length of arc in DEGREESrees

        for i in range(self.n - 1):            
            new_path = path.copy()
            new_path.set_color_by_gradient([self.colors[symbol_n[i]]])

            # hint for future reference
            # p0 = start point (current numbered arc)
            # p1 = end point (next numbered arc)
            # h = handle point (ORIGIN)

            # TODO: make better code

            p0 = curve_dots1[symbol_n[i]].get_center()
            curve_pointer[symbol_n[i + 1]] = -(0.01 * (i + 1) % len_of_arc) * DEGREES
            curve_dots1[symbol_n[i + 1]] = curve_dots[symbol_n[i + 1]].copy().rotate(
                curve_pointer[symbol_n[i + 1]],
                about_point=ORIGIN
            )

            p1 = curve_dots1[symbol_n[i + 1]].get_center()
            h = ORIGIN

            # here comes a little cheating
            # eliminating all curves which starts and ends at same numbered arcs
            # and which crosse ORIGIN.
            # TODO: think of a right way to bend the curve around ORIGIN more efficiently

            if symbol_n[i] != symbol_n[i + 1]:
                coef = abs(symbol_n[i+1] - symbol_n[i])
                
                points = [bezier([p0, normalize(p0+p1), p1])(t) for t in np.linspace(0, 1, 3)]

                # if round(points[1][0], ndigits=1) == 0.0 and round(points[1][1], ndigits=1) == 0.0:
                #     points[1] = [ORIGIN]
                    # (normalize(points[0] - points[2]), TAU/4)*.5
                new_path.set_points_smoothly(points).set_stroke(**self.path_config)
            # circle.add(new_path)
            paths.add(new_path)            

        return paths

        # Here comes the amazing part: Animaaattiooooooon!!
        # frame = self.camera
        # frame.set_width(2 * self.circle.get_width())

    def construct(self):
        # some constants
        
        self.draw_sectors_and_symbol()
        paths = self.make_paths()

        for i in range(3):
            paths[i].set_stroke(width=2, opacity= 1)

        # self.play(ScaleInPlace(arcs[3],1.2), run_func = there_and_back, run_time =2,)
        # self.play(arcs[3].animate.scale(1.2).shift(arcs[3].get_center()*.1), rate_func = there_and_back_with_pause, run_time=3)
        self.wait(11)
        self.play(Create(paths[0]))
        self.wait(5)
        self.play(Create(paths[1]))        
        self.play(Create(paths[2]))
        self.wait()
        # self.play(arcs[3].animate.scale(1/1.3))
        
        self.play(Create(paths[3:]), *(paths[i].animate.set_stroke(**self.path_config) for i in range(3)), run_time=20, rate_func=smoothererstep)
        # self.play(frame.animate.set_width(2 * symbol.get_width()), run_time=3)
        self.wait(3)

        self.play(
            *[FadeOut(mob)for mob in self.mobjects],
            # All mobjects in the screen are saved in self.mobjects
            run_time=2
        )
        self.wait()
        
    
        

        
class EulerArt(PiCircle):
    def setup(self):
        super().setup()    
        MONOKAI_BGGRAY= ManimColor("#272822")
        MONOKAI_PURPLE = ManimColor("#AE81FF") 
        MONOKAI_Comment = ManimColor("#75715E")
        MONOKAI_WHITE= ManimColor("#F8F8F2")
        MONOKAI_RED =	ManimColor("#F92772")
        MONOKAI_YELLOW = ManimColor("#E6DB74")
        MONOKAI_BLUE = ManimColor("#66D9EF")
        MONOKAI_GREEN =	ManimColor("#A6E22E")
        self.symbol = MathTex("e", font_size=72)
        config.background_color = MONOKAI_BGGRAY
        self.n = 3150
        self.path_config = {
            'width':1,
            'opacity':.1
            } # another combination is 1, 0.1

        self.colors = [
            MONOKAI_BGGRAY,
            MONOKAI_GREEN,
            MONOKAI_WHITE,
            MONOKAI_RED,
            MONOKAI_BLUE,
            MONOKAI_PURPLE,
            MONOKAI_YELLOW,
            MONOKAI_Comment,
            TEAL,
            MAROON
            ]
    
    def get_n_digits_of_symbol(self, n):
        mp.dps = n
        return [2] + [int(i) for i in list(str(mp.exp(1)))[2:]]
    
    def construct(self):        
        # self.camera.background_color = self.colors[0]
        self.draw_sectors_and_symbol()
        paths = self.make_paths()

        self.play(Create(paths), *(paths[i].animate.set_stroke(**self.path_config) for i in range(3)), run_time=20, rate_func=smoothererstep)
        # self.play(frame.animate.set_width(2 * symbol.get_width()), run_time=3)
        self.wait(3)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects],
            # All mobjects in the screen are saved in self.mobjects
            run_time=2
        )
        self.wait()



class GoldenArt(PiCircle):
    def setup(self):
        super().setup()
        Q_RED= ManimColor("#ce4327")
        Q_ORANGE= ManimColor("#fdbe2d")
        Q_PURPLE = ManimColor("#702c90") 
        Q_PINK = ManimColor("#f190bd")
        Q_GREEN =	ManimColor("#01a57d")
        Q_WHITE = ManimColor("#d9f0fb")
        Q_BLUE = ManimColor("#0c5dae")
        Q_LIGHT_BLUE =	ManimColor("#47a5dc")
        Q_GREEN = ManimColor("#7fa842")
        Q_YELLOW = ManimColor("#fcf14b")
        self.symbol = MathTex("\\varphi", font_size=72)
        self.n = 6300
        self.path_config = {
            'width':.7,
            'opacity':.2
            } # another combination is 1, 0.1

        self.colors = [
            # sol_base03,
            # sol_base02,
            sol_red,
            sol_base01,
            # sol_base00,
            # sol_base0,
            # sol_base1,
            # sol_base2,
            sol_green,
            sol_base3,
            sol_orange,
            sol_blue,
            sol_yellow,
            sol_magenta,
            sol_violet,
            sol_cyan,
            ]
    
    def get_n_digits_of_symbol(self, n):
        mp.dps = n
        phi = ( mp.sqrt(5) - 1)/2
        return [0] + [int(i) for i in list(str(phi))[2:]]
    def construct(self):        
        self.draw_sectors_and_symbol()
        paths = self.make_paths()

        self.play(Create(paths[3:]), *(paths[i].animate.set_stroke(**self.path_config) for i in range(3)), run_time=20, rate_func=smoothererstep)
        # self.play(frame.animate.set_width(2 * symbol.get_width()), run_time=3)
        self.wait(3)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects],
            # All mobjects in the screen are saved in self.mobjects
            run_time=2
        )
        self.wait()
        

