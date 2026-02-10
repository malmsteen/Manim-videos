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


m1 = 1.0
m2 = 1.0
m3 = 1.0
z = 0.0
# Position
r_1 = [-1, 0.0]
r_2 = [1, 0.0]
r_3 = [0.0, 0.0]

# Velocity
v1 = 0.347111
v2 = 0.532728
x_dot1 = [v1, v2]
x_dot2 = [v1, v2]
x_dot3 = [-2 * v1, -2 * v2]
period = 30

# http://three-body.ipb .ac.rs/bsol.php?id=1
# Brouce A 2
# r_1 = (0.3361300950, 0)
# r_2 = (0.7699893804, 0)
# r_3 = (-1.1061194753, 0)
# x_dot1 = (0, 1.5324315370)
# x_dot2 = (0, -0.6287350978)
# x_dot3 = (0, -0.9036964391)
# period = 7.702408
eps = 1e-3

initial_conditions = np.array(
    [
        r_1,
        r_2,
        r_3,
        x_dot1,
        x_dot2,
        x_dot3,
    ]
).ravel()


def system_odes(t, S, m1=m1, m2=m2, m3=m3):
    p1, p2, p3 = S[0:2], S[2:4], S[4:6]
    dp1_dt, dp2_dt, dp3_dt = S[6:8], S[8:10], S[10:12]

    f1, f2, f3 = dp1_dt, dp2_dt, dp3_dt

    df1_dt = (
        m3 * (p3 - p1) / np.linalg.norm(p3 - p1) ** 3
        + m2 * (p2 - p1) / np.linalg.norm(p2 - p1) ** 3
    )
    df2_dt = (
        m3 * (p3 - p2) / np.linalg.norm(p3 - p2) ** 3
        + m1 * (p1 - p2) / np.linalg.norm(p1 - p2) ** 3
    )
    df3_dt = (
        m1 * (p1 - p3) / np.linalg.norm(p1 - p3) ** 3
        + m2 * (p2 - p3) / np.linalg.norm(p2 - p3) ** 3
    )

    return np.array([f1, f2, f3, df1_dt, df2_dt, df3_dt]).ravel()


def ode_solution_points(function, state0, time, dt=eps):
    solution = solve_ivp(
        function, t_span=(0, time), y0=state0, t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


# points = [initial_conditions]
# num = 1e6
# eps = 1 / num
# dp = period / num
# for i in range(1, int(num)):
#     tmp = ode_solution_points(system_odes, initial_conditions, dp)
#     initial_conditions = tmp[-1]
#     if i % 1000 != 0:
#         continue
#     # print(len(tmp))
#     # print(tmp[-1])
#     # print(tmp[0])
#     # print(type(tmp))
#     points.append(tmp[-1])

#     del tmp

# def for_later():
#     tail = VGroup(TracingTail(dot, time_traced=3).match_color(dot) for dot in dots)


class ThreeBodies(Scene):
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
        lim = 5
        axes = Axes(
            x_range=(-lim, lim, 5),
            y_range=(-lim, lim, 5),
            width=16,
            height=16,
        )
        axes.set_width(FRAME_WIDTH * 0.6)
        axes.center()

        self.play(AnimationGroup(FadeIn(tglogo)))

        # Compute a set of solutions
        # colors = color_gradient([BLUE_E, BLUE_A], len(states))

        curves = VGroup()

        points = ode_solution_points(system_odes, initial_conditions, period)
        print("type(points): ", type(points))
        curve1 = points[:][0:3]
        curve2 = points[:][3:6]
        curve3 = points[:][6:9]
        points
        colors = [RED, GREEN, BLUE]
        for i, color in enumerate(colors):
            curve = VMobject().set_points_smoothly(
                axes.c2p(*points.T[:][i * 2 : (i + 1) * 2])
            )
            curve.set_stroke(color, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=0.5, opacity=1)
        print(axes.c2p(*points.T))
        # pp = [p for p in axes.c2p(*points.T)]
        # pp = pp[:50:10]

        # Display dots moving along those trajectories
        dots = Group(GlowDot(color=color, radius=0.25) for color in colors)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(TracingTail(dot, time_traced=5).match_color(dot) for dot in dots)
        # self.frame.set_focal_distance(10)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)

        curves.scale(4)

        self.play(
            *(ShowCreation(curve, rate_func=linear) for curve in curves),
            run_time=60,
        )
