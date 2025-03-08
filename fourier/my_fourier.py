# Code to draw cool things using the math of complex Fourier-series
# This is an updated version of the code from youtuber Theorem of Beethoven as seen here:
# Theorem of Beethoven link:    https://www.youtube.com/watch?v=2tTshwWTEic
# Adapted from CairoManim to ManimCE
# Inspired by brilliant math youtuber 3Blue1Brown, creator of the Manim Python library:
# 3lue1Brown link:              https://www.youtube.com/watch?v=r6sGWTCMz2k

from manim import *
import numpy as np
# import timeit
import itertools as it

# config.use_opengl_renderer = True

class FourierSceneAbstract(ZoomedScene):
    def __init__(self):
        super().__init__()
        self.fourier_symbol_config = {
            "stroke_width": 1,
            "fill_opacity": 1,
            "height": 4,
        }
        self.vector_config = {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.4
        }
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
            "color": BLUE
        }
        self.n_vectors = 150
        self.cycle_seconds = 5
        self.slow_factor = .25
        self.parametric_func_step = 0.001   
        self.drawn_path_stroke_width = 2
        self.drawn_path_color = RED
        self.drawn_path_interpolation_config = [0, 1]
        self.path_n_samples = 1000
        self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1, 1))
        self.freqs.sort(key=abs)
        self.rect_scale_factor = .1
        self.rect_stroke_width=1
        

    def setup(self):
        super().setup()        
        self.slow_factor_tracker = ValueTracker(self.slow_factor)
        self.vector_clock = ValueTracker(0)
        self.add(self.vector_clock)        
        

    def start_vector_clock(self):           # This updates vector_clock to follow the add_updater parameter dt
        self.vector_clock.add_updater(
        lambda t, dt: t.increment_value(dt * self.slow_factor_tracker.get_value() / self.cycle_seconds)
    )

    
    def stop_vector_clock(self):
        self.vector_clock.remove_updater(self.start_vector_clock)

    def get_fourier_coefs(self, path):
        dt = 1 / self.path_n_samples
        t_range = np.arange(0, 1, dt)

        points = np.array([
            path.point_from_proportion(t)
            for t in t_range
        ])
        complex_points = points[:, 0] + 1j * points[:, 1]

        coefficients = [
            np.sum(np.array([
                c_point * np.exp(-TAU * 1j * freq * t) * dt
                for t, c_point in zip(t_range, complex_points)
                ]))
            for freq in self.freqs
        ]
        return coefficients

    def get_fourier_vectors(self, path):
        coefficients = self.get_fourier_coefs(path)
        
        vectors = VGroup()
        v_is_first_vector = True
        for coef, freq in zip(coefficients,self.freqs):
            v = Vector([np.real(coef), np.imag(coef)], **self.vector_config)
            if v_is_first_vector:
                center_func = VectorizedPoint(ORIGIN).get_location # Function to center position at tip of last vector
                v_is_first_vector = False
            else:
                center_func = last_v.get_end
            v.center_func = center_func
            last_v = v
            v.freq = freq
            v.coef = coef
            v.phase = np.angle(coef)
            v.shift(v.center_func()-v.get_start())
            v.set_angle(v.phase)
            vectors.add(v)
        return vectors

    def update_vectors(self, vectors):
            for v in vectors:
                time = self.vector_clock.get_value()
                v.shift(v.center_func()-v.get_start())
                v.set_angle(v.phase + time * v.freq * TAU)  # NOTE Rotate() did not work here for unknown reason, probably related to how manin handles updaters
              
    def get_circles(self, vectors):
        circles = VGroup()
        for v in vectors:
            c = Circle(radius = v.get_length(), **self.circle_config)
            c.center_func = v.get_start
            c.move_to(c.center_func())
            circles.add(c)
        return circles

    def update_circles(self, circles):
        for c in circles:
            c.move_to(c.center_func())
            
    def get_drawn_path(self, vectors):    # TODO Find out application of None, is for placeholder, may be how keyword argument default is set

        def fourier_series_func(t):
            fss = np.sum(np.array([
                v.coef * np.exp(TAU * 1j * v.freq * t)
                for v in vectors
            ]))
            real_fss = np.array([np.real(fss), np.imag(fss), 0])
            return real_fss
        
        t_range = np.array([0, 1, self.parametric_func_step])
        vector_sum_path = ParametricFunction(fourier_series_func, t_range = t_range)
        broken_path = CurvesAsSubmobjects(vector_sum_path)
        broken_path.stroke_width = 0
        broken_path.start_width = self.drawn_path_interpolation_config[0]
        broken_path.end_width = self.drawn_path_interpolation_config[1]
        return broken_path

    def update_path(self, broken_path):
        alpha = self.vector_clock.get_value()
        n_curves = len(broken_path)
        alpha_range = np.linspace(0, 1, n_curves)
        for a, subpath in zip(alpha_range, broken_path):
            b = (alpha - a)
            if b < 0:
                width = 0
            else:
                width = self.drawn_path_stroke_width * interpolate(broken_path.start_width, broken_path.end_width, (1 - (b % 1)))
            subpath.set_stroke(width=width)


class FourierScene(FourierSceneAbstract):
    def __init__(self):
        super().__init__()

    def get_tex_symbol(self, symbol, color = None):
        symbol = Tex(symbol, **self.fourier_symbol_config)
    
        if (color is not None):
            symbol.set_color(color)

        return symbol

    def get_path_from_symbol(self, symbol):
        return symbol.family_members_with_points()[0]

    def construct(self):
        # Symbols to draw
        symbol = self.get_tex_symbol(r'\rm M', RED)
        # symbol2 = self.get_tex_symbol("e", BLUE)
        group = VGroup(symbol).arrange(RIGHT)

        # Fourier series for symbol
        vectors = self.get_fourier_vectors(self.get_path_from_symbol(symbol))
        circles = self.get_circles(vectors)
        drawn_path1 = self.get_drawn_path(vectors).set_color(RED)

      



        # Fourier series for symbol2
        # vectors2 = self.get_fourier_vectors(self.get_path_from_symbol(symbol2))
        # circles2 = self.get_circles(vectors2)
        # drawn_path2 = self.get_drawn_path(vectors2).set_color(BLUE)

        # Text definition
        # text = Tex("hire", fill_opacity = 1, height = 3)
        # text.next_to(group, LEFT*1.4)

        # all_mobs = VGroup(group, text)
        all_mobs = VGroup(group)

        # Camera updater
        last_vector = vectors[-1]

        def follow_end_vector(camera): 
            camera.move_to(last_vector.get_end())

        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors]
                for arrow in vector_group
            ],
            *[
                Create(circle)
                for circle_group in [circles]
                for circle in circle_group
            ],
            run_time=2.5,
        )

        # Add objects to scene
        self.add( 
            vectors,
            circles,
            drawn_path1.set_stroke(width = 0),            
        )

        # Camera move
        # self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)

        # Add updaters and start vector clock
        # self.camera.frame.add_updater(follow_end_vector)
        vectors.add_updater(self.update_vectors)
        circles.add_updater(self.update_circles)
        # vectors2.add_updater(self.update_vectors)
        # circles2.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        # drawn_path2.add_updater(self.update_path)
        self.start_vector_clock()

        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        # Move camera then write text
        # self.camera.frame.remove_updater(follow_end_vector)
        # self.play(
            # self.camera.frame.animate.set_width(all_mobs.width * 1.5).move_to(all_mobs.get_center()),
            # Write(text),
            # run_time = 1 * self.cycle_seconds,
        # )
        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.5 * self.cycle_seconds)
        
        # Remove updaters so can animate
        self.stop_vector_clock()
        drawn_path1.clear_updaters()
        # drawn_path2.clear_updaters()
        vectors.clear_updaters()
        # vectors2.clear_updaters()
        circles.clear_updaters()
        # circles2.clear_updaters()

        self.play(
            *[
                Uncreate(vmobject)
                for vgroup in [vectors, circles]
                for vmobject in vgroup
            ],
            FadeOut(drawn_path1),
            FadeIn(symbol),
            run_time = 2.5,
        )

        self.wait(3)



class FourierSeriesExampleWithRectForZoom(FourierScene):    
    def __init__(self):
        super().__init__()
        self.n_vectors = 100
        self.cycle_seconds = 5
        self.slow_factor = .25       
        self.rect_stroke_width=1
        self.file_name = None

    def get_shape(self):
        shape = SVGMobject(self.file_name)
        return shape

    def get_path(self):
        shape = self.get_shape()
        path = shape.family_members_with_points()[0]
        path.set_height(self.height)
        path.set_fill(opacity=0)
        path.set_stroke(WHITE, 0)
        return path
    
    def get_rect_center(self, vectors):
        return center_of_mass([
            v.get_end()
            for v in vectors
        ])

    def get_rect(self):
        return ScreenRectangle(
            color=BLUE,
            stroke_width=self.rect_stroke_width,
        )       

    def run_one_cycle(self):
        time = 1 / self.slow_factor
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                # mcsw / np.sqrt(k),
                mcsw / k,
                mcsw,
            ))
        return circles

    def construct(self):
        
        symbol = self.get_tex_symbol(r"\rm M", RED) 
        group = VGroup(symbol).arrange(RIGHT)  

        vectors = self.get_fourier_vectors(self.get_path_from_symbol(symbol))
        circles = self.get_circles(vectors)
        drawn_path1 = self.get_drawn_path(vectors).set_color(RED)
        
        # self.add_vectors_circles_path()
        # self.circles.set_stroke(opacity=0.5)
        rect = self.rect = self.get_rect()
        rect.set_height(self.rect_scale_factor * config.frame_height)
        rect.add_updater(lambda m: m.move_to(
            self.get_rect_center(vectors)
        ))

          # Fourier series for symbol2
        # vectors2 = self.get_fourier_vectors(self.get_path_from_symbol(symbol2))
        # circles2 = self.get_circles(vectors2)
        # drawn_path2 = self.get_drawn_path(vectors2).set_color(BLUE)

        # Text definition
        # text = Tex("hire", fill_opacity = 1, height = 3)
        # text.next_to(group, LEFT*1.4)

        # all_mobs = VGroup(group, text)
        all_mobs = VGroup(group)

        # Camera updater
        last_vector = vectors[-1]

        # def follow_end_vector(camera): 
        #     camera.move_to(last_vector.get_end())

        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors]
                for arrow in vector_group
            ],
            *[
                Create(circle)
                for circle_group in [circles]
                for circle in circle_group
            ],
            run_time=2.5,
        )

        # Add objects to scene
        self.add( 
            vectors,
            circles,
            drawn_path1.set_stroke(width = 0),            
        )

        
        
        self.add(rect)
        

        # Camera move
        # self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)

        # Add updaters and start vector clock
        # self.camera.frame.add_updater(follow_end_vector)
        vectors.add_updater(self.update_vectors)
        circles.add_updater(self.update_circles)
        # vectors2.add_updater(self.update_vectors)
        # circles2.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        # drawn_path2.add_updater(self.update_path)
        self.start_vector_clock()

        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        # Move camera then write text
        # self.camera.frame.remove_updater(follow_end_vector)
        # self.play(
            # self.camera.frame.animate.set_width(all_mobs.width * 1.5).move_to(all_mobs.get_center()),
            # Write(text),
            # run_time = 1 * self.cycle_seconds,
        # )
        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.5 * self.cycle_seconds)
        
        # Remove updaters so can animate
        self.stop_vector_clock()
        drawn_path1.clear_updaters()
        # drawn_path2.clear_updaters()
        vectors.clear_updaters()
        # vectors2.clear_updaters()
        circles.clear_updaters()
        # circles2.clear_updaters()

        self.play(
            *[
                Uncreate(vmobject)
                for vgroup in [vectors, circles]
                for vmobject in vgroup
            ],
            FadeOut(drawn_path1),
            FadeIn(symbol),
            run_time = 2.5,
        )

        self.wait(3)
        # self.run_one_cycle()   


class ZoomedInFourierSeriesExample(FourierSeriesExampleWithRectForZoom, MovingCameraScene):
    def __init__(self):
        super().__init__()
        # self.vector_config = {
        #     "max_tip_length_to_length_ratio": 0.15,
        #     "tip_length": 0.05,
        #     }
        self.parametric_function_step_size = 0.001    
        self.zoomed_display_height = 2 # self.rect_scale_factor * config.frame_height
        self.zoomed_display_width = 16 / 9 * self.zoomed_display_height
    # def setup(self):
    #     FourierScene.setup(self)
    #     MovingCameraScene.setup(self)
    
    # def get_rect(self):
    #     return self.camera
    
    def construct(self):
        # Symbols to draw
        symbol = self.get_tex_symbol(r'\rm M', RED)
        # symbol2 = self.get_tex_symbol("e", BLUE)
        group = VGroup(symbol).arrange(RIGHT)

        # Fourier series for symbol
        vectors = self.get_fourier_vectors(self.get_path_from_symbol(symbol))
        circles = self.get_circles(vectors)
        drawn_path1 = self.get_drawn_path(vectors).set_color(RED)

    
        all_mobs = VGroup(group)

        # Camera updater
        last_vector = vectors[-1]

        def follow_end_vector(camera): 
            camera.move_to(last_vector.get_end())

        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors]
                for arrow in vector_group
            ],
            *[
                Create(circle)
                for circle_group in [circles]
                for circle in circle_group
            ],
            run_time=2.5,
        )

        rect = self.rect = self.get_rect()
        rect.set_height(self.rect_scale_factor * config.frame_height)
        rect.add_updater(lambda m: m.move_to(
            self.get_rect_center(vectors)
        ))

        # Add objects to scene
        self.add( 
            vectors,
            circles,
            drawn_path1.set_stroke(width = 0), 
            rect           
        )

        # Camera move
        # self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)

        # Add updaters and start vector clock
        # self.camera.frame.add_updater(follow_end_vector)
        vectors.add_updater(self.update_vectors)
        circles.add_updater(self.update_circles)
        # vectors2.add_updater(self.update_vectors)
        # circles2.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        # drawn_path2.add_updater(self.update_path)
        self.start_vector_clock()

        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        # Move camera then write text
        # self.camera.frame.remove_updater(follow_end_vector)
        # self.play(
            # self.camera.frame.animate.set_width(all_mobs.width * 1.5).move_to(all_mobs.get_center()),
            # Write(text),
            # run_time = 1 * self.cycle_seconds,
        # )

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(self.get_rect_center(vectors))
        frame.frame_width = rect.width
        frame.frame_height = rect.height 
        frame.add_updater(lambda m: m.move_to(rect))  
        
        # frame.stretch_to_fit_height(rect)

        # frame.set_color(BLUE)
        # zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))
                
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        self.cycle_seconds += 10
        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.1 * self.cycle_seconds)
        self.wait()
        


        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.1 * self.cycle_seconds)
        self.wait()


      
        # zoomed_camera_text.next_to(zoomed_display_frame, DOWN)
        # Remove updaters so can animate
        self.stop_vector_clock()
        drawn_path1.clear_updaters()
        # drawn_path2.clear_updaters()
        vectors.clear_updaters()
        # vectors2.clear_updaters()
        circles.clear_updaters()
        # circles2.clear_updaters()

        self.play(
            *[
                Uncreate(vmobject)
                for vgroup in [vectors, circles]
                for vmobject in vgroup
            ],
            FadeOut(drawn_path1),
            FadeIn(symbol),
            run_time = 2.5,
        )

        self.wait(3)


    

        
        



            