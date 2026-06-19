from manim import *
from scipy.integrate import solve_ivp

SCALE_FACTOR = 1
tmp = config.pixel_height
config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
config.frame_height = config.frame_height / SCALE_FACTOR
config.frame_width = config.frame_height * 9 / 16
FRAME_HEIGHT = config.frame_height
FRAME_WIDTH = config.frame_width

config.background_color = "#080404"


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function, t_span=(0, time), y0=state0, t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


# def for_later():
#     tail = VGroup(TracingTail(dot, time_traced=3).match_color(dot) for dot in dots)


class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.set_camera_orientation(
            phi=65 * DEGREES, theta=30 * DEGREES, gamma=0 * DEGREES
        )
        self.begin_ambient_camera_rotation(rate=0.05)  # Start move camera
        self.add(axes)

        # # Add the equations
        # equations = Tex(
        #     R"""
        #     \begin{aligned}
        #     \frac{\mathrm{d} x}{\mathrm{~d} t} & =\sigma(y-x) \\
        #     \frac{\mathrm{d} y}{\mathrm{~d} t} & =x(\rho-z)-y \\
        #     \frac{\mathrm{d} z}{\mathrm{~d} t} & =x y-\beta z
        #     \end{aligned}
        #     """,
        #     t2c={
        #         "x": RED,
        #         "y": GREEN,
        #         "z": BLUE,
        #     },
        #     font_size=30,
        # )
        # equations.fix_in_frame()
        # equations.to_corner(UL)
        # equations.set_backstroke()
        # self.play(Write(equations))

        # Compute a set of solutions
        epsilon = 1e-5
        evolution_time = 60
        n_points = 10
        states = [[10, 10, 10 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=1.5, opacity=1)

        # Display dots moving along those trajectories
        dots = Group(Dot(color=color, radius=0.25) for color in colors)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracedPath(dot, dissipating_time=3).match_color(dot) for dot in dots
        )

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        self.play(
            *(Create(curve, rate_func=linear) for curve in curves),
            run_time=evolution_time,
        )
