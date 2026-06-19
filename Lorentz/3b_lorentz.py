from manimlib import *
from scipy.integrate import solve_ivp

SCALE_FACTOR = 1
# tmp = config.pixel_height
# config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
# config.frame_height = config.frame_height / SCALE_FACTOR
# config.frame_width = config.frame_height * 9 / 16
# FRAME_HEIGHT = config.frame_height
# FRAME_WIDTH = config.frame_width

DEFAULT_PIXEL_HEIGHT, DEFAULT_PIXEL_WIDTH = DEFAULT_PIXEL_WIDTH, DEFAULT_PIXEL_HEIGHT
ASPECT_RATIO = 9.0 / 16.0
FRAME_HEIGHT = 16.0
FRAME_WIDTH = FRAME_HEIGHT * ASPECT_RATIO

RED1 = "#d13925"
сс = ["#FFDF00", "#B87333", "#804A00", "#4E2C00"]
# config.background_color = "#080404"


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def get_vel_accel(state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt, dydt, dzdt = lorenz_system(state, sigma, rho, beta)
    ax = sigma * (dydt - dxdt)
    ay = dxdt * (rho - z) - x * dzdt - dydt
    az = dxdt * y + x * dydt - beta * dzdt
    return (dxdt, dydt, dzdt), (ax, ay, az)


def calc_frenet(vel, accel):
    v = np.linalg.norm(vel)
    a = np.linalg.norm(accel)
    binormal = np.linalg.norm(np.cross(v, a))
    normal = np.cross(binormal, v)
    return v, normal, binormal


def to_frenet(m, dt, point, norm_vel, norm_accel):
    c = point.get_center()


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function, t_span=(0, time), y0=state0, t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


def for_later():
    tail = VGroup(TracingTail(dot, time_traced=3).match_color(dot) for dot in dots)


class Intro(Scene):
    def construt(self):

        state = [10, 10, 10]
        pp = [np.array(state)]
        dt = 0.1
        for _ in range(10):
            v = lorenz_system(_, state)
            p = v * dt
            pp.append(p)

        gd = GlowDot(color=GREEN_SCREEN, radius=0.25).move_to(pp[0])
        tail = TracingTail(gd, time_traced=2).match_color(gd)
        self.play(FadeIn(gd), run_time=2)
        self.add(tail)

        for i in range(1, len(pp)):
            self.play(gd.animate.move_to(pp[i]))
            self.wait()


class LorenzAttractor(Scene):
    def construct(self):

        font = {"fill_color": GREY, "font_size": 12}
        test = ImageMobject("telegram-logo-32.png").scale(0.04)
        # self.add(test)
        tglogo = Group(
            test,
            Text("@math_and_beyond", **font),
        )
        tglogo.arrange(RIGHT, buff=0.1)

        # vglogo = tglogo.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tglogo.fix_in_frame()
        tglogo.to_corner(DR).shift(DR * 0.2)

        # Set up axes
        lim = 30
        axes = ThreeDAxes(
            x_range=(-lim, lim, 5),
            y_range=(-lim, lim, 5),
            z_range=(-0, lim * 1.5, 5),
            width=16,
            height=16,
            depth=12,
        )
        axes.set_width(FRAME_WIDTH * 0.6)
        axes.center().shift(0.5 * IN)

        self.frame.reorient(43, 76, 1, IN, 10)
        self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 8 * DEGREES))
        self.add(axes)

        # Add the equations
        equations = Tex(
            r"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & =\sigma(y-x) \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & =x(\rho-z)-y \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & =x y-\beta z
            \end{aligned}
            """,
            t2c={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=30,
        )
        equations.fix_in_frame()
        equations.to_edge(DOWN).shift(0.5 * UP)
        equations.set_backstroke()
        self.play(AnimationGroup(Write(equations, run_time=3), FadeIn(tglogo)))

        # Compute a set of solutions
        epsilon = 1e-8
        evolution_time = 60
        n_points = 10
        states = [[10, 10, 10 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))
        # grad = [YELLOW_E, "#FFDF00", "#B87333", "#804A00", RED1, RED]
        colors = color_gradient(colors, len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 0.5, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=0.5, opacity=1)
        print(axes.c2p(*points.T))
        pp = [p for p in axes.c2p(*points.T)]
        pp = pp[:50:10]

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0.15) for color in colors)
        gd = GlowDot(color=GREEN_SCREEN).move_to(pp[0])
        tt = TracingTail(gd, time_traced=2).match_color(gd)

        # self.play(FadeIn(gd), run_time=2)
        # self.add(tt)
        # for i in range(1, len(pp)):
        #     self.play(gd.animate.move_to(pp[i]))
        #     self.wait()

        # self.wait(5)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracingTail(dot, time_traced=5, stroke_width=1).match_color(dot)
            for dot in dots
        )
        self.frame.set_focal_distance(10)

        # def update_camera(cam, dots=dots):
        #     self.camera.frame.move_to(dots[0].get_center())
        #     cam.reorient(43, 76, 1, dots[0].get_center(), 0.1)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        # self.frame.clear_updaters()
        # self.frame.add_updater(update_camera)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=evolution_time,
        )


def rossler_system(t, state, a=0.2, b=0.2, c=5.7):
    x, y, z = state
    dxdt = -(y +  z)
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]



preamble=r"""
\usepackage[utf8]{inputenc}
\usepackage[]{fontspec}
\setromanfont{STIX Two Text}
\setsansfont{STIX Two Text}
\setmonofont{Anonymous Pro}
\defaultfontfeatures{Ligatures={TeX}}
\setmainfont[]{STIX Two Text}

\usepackage[math-style=TeX]{unicode-math}
\unimathsetup{math-style=TeX}
\setmathfont{texgyrepagella-math.otf}
"""

# template = TexTemplate(
#     preamble=r"""
# \usepackage[utf8]{inputenc}
# \usepackage[T2A]{fontenc}
# \usepackage[russian]{babel}
# \usepackage{amssymb}
# \usepackage{amsmath}
# """
# )


class RosslerAttractor(Scene):
    def construct(self):

        font = {"fill_color": GREY, "font_size": 12, "font": "Anonymous Pro"}        
        test = ImageMobject("telegram-logo-32.png").scale(0.04)
        # self.add(test)
        tglogo = Group(
            test,
            Text("@math_and_beyond", **font),
        )
        tglogo.arrange(RIGHT, buff=0.1)

        # vglogo = tglogo.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tglogo.fix_in_frame()
        tglogo.to_corner(DR).shift(DR * 0.2)

        # Set up axes
        lim = 15

        axes = ThreeDAxes(
            x_range=(-25, 25, 5),
            y_range=(-25, 25, 5),
            z_range=(-5, 30, 5),
            width=12,
            height=12,
            depth=12,
        )
        axes.set_width(FRAME_WIDTH * 0.6)
        axes.center().shift(0.3 * OUT)

        self.frame.reorient(43, 76, 1, IN, 10)
        self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 8 * DEGREES))
        # self.add(axes)

        # Add the equations
        equations = Tex(
            r"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & = -(y + z) \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & = x + ay \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & = b + z(x-c)
            \end{aligned}
            """,
            t2c={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=20,
            # template='basic_ctex',
            # additional_preamble=preamble
            
        )
        equations.fix_in_frame()
        equations.to_edge(DOWN).shift(0.3 * UP)
        equations.set_backstroke()
        

        # Compute a set of solutions
        epsilon = 1e-2
        evolution_time = 240
        n_points = 10
        states = [[1, 1, 1 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))
         
        # a_bb = Tex(r"\mathbb{A}", additional_preamble=preamble)
        # ttractor = Text("ттрактор ", font="STIX Two Text")
        # p_bb = Tex(r"\mathbb{P}", additional_preamble=preamble)
        # ossler = Text("ёсслера", font="STIX Two Text")

        # title = VGroup(a_bb, ttractor, p_bb, ossler).arrange(RIGHT, buff=0.04)    
        title = Text("Аттрактор Рёсслера", font="STIX Two Text", font_size=30)
        title.to_edge(UP, buff=.5)
        title.set_color_by_gradient(BLUE_D, BLUE, BLUE_A, BLUE, BLUE_D)
        title.fix_in_frame()
        
        
        # grad = [YELLOW_E, "#FFDF00", "#B87333", "#804A00", RED1, RED]
        # colors = color_gradient(colors, len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(function=rossler_system, state0=state, time=evolution_time, dt=0.001)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 0.5, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=0.5, opacity=1)
        curves.scale(1.3)
        
        
        
        self.play(
            AnimationGroup(
                Write(equations, run_time=3), 
                FadeIn(tglogo)                
                ),
            LaggedStart(
                *(FadeIn(t) for t in title),
                lag_ratio=.2,
            ),
            run_time=3            
            )
        
        
        print(axes.c2p(*points.T))
        pp = [p for p in axes.c2p(*points.T)]
        pp = pp[:50:10]

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0.2) for color in colors)
        gd = GlowDot(color=GREEN_SCREEN).move_to(pp[0])
        tt = TracingTail(gd, time_traced=2).match_color(gd)

        # self.play(FadeIn(gd), run_time=2)
        # self.add(tt)
        # for i in range(1, len(pp)):
        #     self.play(gd.animate.move_to(pp[i]))
        #     self.wait()

        # self.wait(5)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracingTail(dot, time_traced=10, stroke_width=1).match_color(dot)
            for dot in dots
        )
        self.frame.set_focal_distance(10)

        # def update_camera(cam, dots=dots):
        #     self.camera.frame.move_to(dots[0].get_center())
        #     cam.reorient(43, 76, 1, dots[0].get_center(), 0.1)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        # self.frame.clear_updaters()
        # self.frame.add_updater(update_camera)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=57,
        )
        

def aizawa_system(t, state, a = 0.95, b = 0.7, c = 0.6, d = 3.5, e = 0.25, f = 0.1):
    x, y, z = state
    dxdt = (z - b) * x - d * y
    dydt = d * x + (z - b) * y
    dzdt = c + a * z - z**3/3 - (x**2 + y**2) * (1 + e * z) + f * z * x**3
    return [dxdt, dydt, dzdt]
        
class AizawaAttractor(Scene):
    def construct(self):

        font = {"fill_color": GREY, "font_size": 12, "font": "Anonymous Pro"}        
        test = ImageMobject("telegram-logo-32.png").scale(0.04)
        # self.add(test)
        tglogo = Group(
            test,
            Text("@math_and_beyond", **font),
        )
        tglogo.arrange(RIGHT, buff=0.1)

        # vglogo = tglogo.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tglogo.fix_in_frame()
        tglogo.to_corner(DR).shift(DR * 0.2)

        # Set up axes
        lim = 15

        axes = ThreeDAxes(
            x_range=(-25, 25, 5),
            y_range=(-25, 25, 5),
            z_range=(-5, 30, 5),
            width=12,
            height=12,
            depth=12,
        )
        axes.set_width(FRAME_WIDTH * 0.6)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 8 * DEGREES))
        # self.add(axes)

        # Add the equations
        equations = Tex(
            r"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & = -(y + z) \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & = x + ay \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & = b + z(x-c)
            \end{aligned}
            """,
            t2c={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=20,
            # template='basic_ctex',
            # additional_preamble=preamble
            
        )
        equations.fix_in_frame()
        equations.to_edge(DOWN).shift(0.5 * UP)
        equations.set_backstroke()
        

        # Compute a set of solutions
        epsilon = 1e-2
        evolution_time = 80
        n_points = 10
        states = [[1, 1, 1 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))
         
        # a_bb = Tex(r"\mathbb{A}", additional_preamble=preamble)
        # ttractor = Text("ттрактор ", font="STIX Two Text")
        # p_bb = Tex(r"\mathbb{P}", additional_preamble=preamble)
        # ossler = Text("ёсслера", font="STIX Two Text")

        # title = VGroup(a_bb, ttractor, p_bb, ossler).arrange(RIGHT, buff=0.04)    
        title = Text("Аттрактор Рёслера", font="STIX Two Text", font_size=30)
        title.to_edge(UP, buff=.5)
        title.set_color_by_gradient(BLUE_D, BLUE, BLUE_A, BLUE, BLUE_D)
        title.fix_in_frame()
        
        
        # grad = [YELLOW_E, "#FFDF00", "#B87333", "#804A00", RED1, RED]
        # colors = color_gradient(colors, len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(function=aizawa_system, state0=state, time=evolution_time, dt=0.002)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 0.5, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=0.5, opacity=1)
        curves.scale(1.3)
        
        
        
        self.play(
            AnimationGroup(
                Write(equations, run_time=3), 
                FadeIn(tglogo)                
                ),
            LaggedStart(
                *(FadeIn(t) for t in title),
                lag_ratio=.2,
            ),
            run_time=3            
            )
        
        
        print(axes.c2p(*points.T))
        pp = [p for p in axes.c2p(*points.T)]
        pp = pp[:50:10]

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0.2) for color in colors)
        gd = GlowDot(color=GREEN_SCREEN).move_to(pp[0])
        tt = TracingTail(gd, time_traced=2).match_color(gd)

        # self.play(FadeIn(gd), run_time=2)
        # self.add(tt)
        # for i in range(1, len(pp)):
        #     self.play(gd.animate.move_to(pp[i]))
        #     self.wait()

        # self.wait(5)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracingTail(dot, time_traced=10, stroke_width=1).match_color(dot)
            for dot in dots
        )
        self.frame.set_focal_distance(10)

        # def update_camera(cam, dots=dots):
        #     self.camera.frame.move_to(dots[0].get_center())
        #     cam.reorient(43, 76, 1, dots[0].get_center(), 0.1)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        # self.frame.clear_updaters()
        # self.frame.add_updater(update_camera)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=20,
        )
        
        
        
def halvorsen_system(t, state, a=1.4):
    x, y, z = state
    dxdt = -a*x -4*y -4*z -y**2
    dydt = -a*y - 4*z - 4*x - z**2
    dzdt = -a*z -4*x - 4*y -x**2
    return [dxdt, dydt, dzdt]

class HalvorsenAttractor(Scene):
    def construct(self):

        font = {"fill_color": GREY, "font_size": 12, "font": "Anonymous Pro"}        
        test = ImageMobject("telegram-logo-32.png").scale(0.04)
        # self.add(test)
        tglogo = Group(
            test,
            Text("@math_and_beyond", **font),
        )
        tglogo.arrange(RIGHT, buff=0.1)

        # vglogo = tglogo.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tglogo.fix_in_frame()
        tglogo.to_corner(DR).shift(DR * 0.2)

        # Set up axes
        lim = 15

        axes = ThreeDAxes(
            x_range=(-25, 25, 5),
            y_range=(-25, 25, 5),
            z_range=(-5, 30, 5),
            width=12,
            height=12,
            depth=12,
        )
        axes.set_width(FRAME_WIDTH * 0.6)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 8 * DEGREES))
        # self.add(axes)

        # Add the equations
        equations = Tex(
            r"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & = -a*x -4*y -4*z -y**2 \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & = -a*y - 4*z - 4*x - z**2 \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & = -a*z -4*x - 4*y -x**2
            \end{aligned}
            """,
            t2c={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=20,
            # template='basic_ctex',
            # additional_preamble=preamble
            
        )
        equations.fix_in_frame()
        equations.to_edge(DOWN).shift(0.5 * UP)
        equations.set_backstroke()
        

        # Compute a set of solutions
        epsilon = 1e-2
        evolution_time = 240
        n_points = 10
        states = [[1, 1, 1 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))
         
        # a_bb = Tex(r"\mathbb{A}", additional_preamble=preamble)
        # ttractor = Text("ттрактор ", font="STIX Two Text")
        # p_bb = Tex(r"\mathbb{P}", additional_preamble=preamble)
        # ossler = Text("ёсслера", font="STIX Two Text")

        # title = VGroup(a_bb, ttractor, p_bb, ossler).arrange(RIGHT, buff=0.04)    
        title = Text("Аттрактор Рёслера", font="STIX Two Text", font_size=30)
        title.to_edge(UP, buff=.5)
        title.set_color_by_gradient(BLUE_D, BLUE, BLUE_A, BLUE, BLUE_D)
        title.fix_in_frame()
        
        
        # grad = [YELLOW_E, "#FFDF00", "#B87333", "#804A00", RED1, RED]
        # colors = color_gradient(colors, len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(function=halvorsen_system, state0=state, time=evolution_time, dt=0.002)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 0.5, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=0.5, opacity=1)
        curves.scale(1.3)
        
        
        
        self.play(
            AnimationGroup(
                Write(equations, run_time=3), 
                FadeIn(tglogo)                
                ),
            LaggedStart(
                *(FadeIn(t) for t in title),
                lag_ratio=.2,
            ),
            run_time=3            
            )
        
        
        print(axes.c2p(*points.T))
        pp = [p for p in axes.c2p(*points.T)]
        pp = pp[:50:10]

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0.2) for color in colors)
        gd = GlowDot(color=GREEN_SCREEN).move_to(pp[0])
        tt = TracingTail(gd, time_traced=2).match_color(gd)

        # self.play(FadeIn(gd), run_time=2)
        # self.add(tt)
        # for i in range(1, len(pp)):
        #     self.play(gd.animate.move_to(pp[i]))
        #     self.wait()

        # self.wait(5)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracingTail(dot, time_traced=10, stroke_width=1).match_color(dot)
            for dot in dots
        )
        self.frame.set_focal_distance(10)

        # def update_camera(cam, dots=dots):
        #     self.camera.frame.move_to(dots[0].get_center())
        #     cam.reorient(43, 76, 1, dots[0].get_center(), 0.1)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        # self.frame.clear_updaters()
        # self.frame.add_updater(update_camera)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=57,
        )
        
        

def newton_leipnik_system(t, state, a=1.4):
    x, y, z = state
    dxdt = -a*x + y + 10*y*z
    dydt = -x -0.4*y + 5*x*z
    dzdt = b*z - 5*x*y 
    return [dxdt, dydt, dzdt]

class NewtonLeipnikAttractor(Scene):
    def construct(self):

        font = {"fill_color": GREY, "font_size": 12, "font": "Anonymous Pro"}        
        test = ImageMobject("telegram-logo-32.png").scale(0.04)
        # self.add(test)
        tglogo = Group(
            test,
            Text("@math_and_beyond", **font),
        )
        tglogo.arrange(RIGHT, buff=0.1)

        # vglogo = tglogo.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tglogo.fix_in_frame()
        tglogo.to_corner(DR).shift(DR * 0.2)

        # Set up axes
        lim = 15

        axes = ThreeDAxes(
            x_range=(-25, 25, 5),
            y_range=(-25, 25, 5),
            z_range=(-5, 30, 5),
            width=12,
            height=12,
            depth=12,
        )
        axes.set_width(FRAME_WIDTH * 0.6)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 8 * DEGREES))
        # self.add(axes)

        # Add the equations
        equations = Tex(
            r"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & = -ax + y + 10yz \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & = -x -0.4y + 5xz \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & = bz - 5xy
            \end{aligned}
            """,
            t2c={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=20,
            # template='basic_ctex',
            # additional_preamble=preamble
            
        )
        equations.fix_in_frame()
        equations.to_edge(DOWN).shift(0.5 * UP)
        equations.set_backstroke()
        

        # Compute a set of solutions
        epsilon = 1e-2
        evolution_time = 240
        n_points = 10
        states = [[1, 1, 1 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))
         
        # a_bb = Tex(r"\mathbb{A}", additional_preamble=preamble)
        # ttractor = Text("ттрактор ", font="STIX Two Text")
        # p_bb = Tex(r"\mathbb{P}", additional_preamble=preamble)
        # ossler = Text("ёсслера", font="STIX Two Text")

        # title = VGroup(a_bb, ttractor, p_bb, ossler).arrange(RIGHT, buff=0.04)    
        title = Text("Аттрактор Рёслера", font="STIX Two Text", font_size=30)
        title.to_edge(UP, buff=.5)
        title.set_color_by_gradient(BLUE_D, BLUE, BLUE_A, BLUE, BLUE_D)
        title.fix_in_frame()
        
        
        # grad = [YELLOW_E, "#FFDF00", "#B87333", "#804A00", RED1, RED]
        # colors = color_gradient(colors, len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(function=newton_leipnik_system,     state0=state, time=evolution_time, dt=0.002)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 0.5, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=0.5, opacity=1)
        curves.scale(1.3)
        
        
        
        self.play(
            AnimationGroup(
                Write(equations, run_time=3), 
                FadeIn(tglogo)                
                ),
            LaggedStart(
                *(FadeIn(t) for t in title),
                lag_ratio=.2,
            ),
            run_time=3            
            )
        
        
        print(axes.c2p(*points.T))
        pp = [p for p in axes.c2p(*points.T)]
        pp = pp[:50:10]

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0.2) for color in colors)
        gd = GlowDot(color=GREEN_SCREEN).move_to(pp[0])
        tt = TracingTail(gd, time_traced=2).match_color(gd)

        # self.play(FadeIn(gd), run_time=2)
        # self.add(tt)
        # for i in range(1, len(pp)):
        #     self.play(gd.animate.move_to(pp[i]))
        #     self.wait()

        # self.wait(5)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracingTail(dot, time_traced=10, stroke_width=1).match_color(dot)
            for dot in dots
        )
        self.frame.set_focal_distance(10)

        # def update_camera(cam, dots=dots):
        #     self.camera.frame.move_to(dots[0].get_center())
        #     cam.reorient(43, 76, 1, dots[0].get_center(), 0.1)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        # self.frame.clear_updaters()
        # self.frame.add_updater(update_camera)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=57,
        )
