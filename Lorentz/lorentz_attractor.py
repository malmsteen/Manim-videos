from manim import *
import numpy as np

MONOKAI_PINK = "#f92672"
MONOKAI_BLUE = "#66d9ef"
MONOKAI_ORANGE = "#fd971f"
MONOKAI_GREEN = "#a6e22e"
MONOKAI_PURPLE = "#ae81ff"


class Lorenz_Attractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            z_range=[0, 6, 1],
            axis_config={"include_tip": True, "include_ticks": True, "stroke_width": 1},
        )
        # axes.shift(2*DOWN)
        dot = Sphere(radius=0.05, fill_color=BLUE).move_to(
            0 * RIGHT + 0.1 * UP + 0.105 * OUT
        )

        self.set_camera_orientation(
            phi=65 * DEGREES, theta=30 * DEGREES, gamma=0 * DEGREES
        )
        self.begin_ambient_camera_rotation(rate=0.05)  # Start move camera

        dtime = 0.1
        numsteps = 30

        self.add(axes, dot)

        def lorenz(x, y, z, s=10, r=28, b=8.0 / 2.0):
            x_dot = s * (y - x)
            y_dot = r * x - y - x * z
            z_dot = x * y - b * z
            return x_dot, y_dot, z_dot

        def update_trajectory(mob, dt):
            new_point = dot.get_center()
            if np.linalg.norm(new_point - self.points[-1]) > 0.01:
                mob.add_smooth_curve_to(new_point)

        traj = VMobject()
        traj.start_new_path(dot.get_center())
        traj.set_stroke(MONOKAI_PINK, 1.5, opacity=0.8)
        traj.shift(2 * DOWN)
        traj.add_updater(update_trajectory)
        self.add(traj)

        def update_position(mob, dt):
            x_dot, y_dot, z_dot = lorenz(
                dot.get_center()[0] * 10,
                dot.get_center()[1] * 10,
                dot.get_center()[2] * 10,
            )
            x = x_dot * dt / 10
            y = y_dot * dt / 10
            z = z_dot * dt / 10
            mob.shift(x / 10 * RIGHT + y / 10 * UP + z / 10 * OUT)

        dot.add_updater(update_position)
        self.wait(30)


