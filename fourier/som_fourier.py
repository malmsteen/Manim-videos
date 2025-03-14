
# Adapted from CairoManim to ManimCE
# Inspired by brilliant math youtuber 3Blue1Brown, creator of the Manim Python library:
# 3lue1Brown link:              https://www.youtube.com/watch?v=r6sGWTCMz2k

from manim import *
import numpy as np
import itertools as it
# import timeit

config.use_opengl_renderer = True

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
            "max_tip_length_to_length_ratio": 0.15,
            "tip_length": 0.1,
            "max_stroke_width_to_length_ratio": 8,
            "stroke_width": 1
        }
        self.scaled_vector_config ={
            "stroke_width":.1,            
            "max_tip_length_to_length_ratio": 0.15,
            "tip_length": 0.05,
        }    
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 0.75,
            "color": BLUE
        }
        self.max_circle_stroke_width = 1
        self.n_vectors = 101
        self.cycle_seconds = 15
        self.slow_factor = 1
        self.parametric_func_step = 0.001   
        self.drawn_path_stroke_width = 4
        self.drawn_path_interpolation_config = [0, 1]
        self.path_n_samples = 1000
        self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1, 1))
        self.freqs.sort(key=abs)

    def setup(self):
        super().setup()
        self.vector_clock = ValueTracker(0)
        self.slow_factor_tracker = ValueTracker(self.slow_factor)
        self.add(self.vector_clock)

    def start_vector_clock(self):           # This updates vector_clock to follow the add_updater parameter dt
        self.vector_clock.add_updater(
            lambda t, dt: t.increment_value(dt * self.slow_factor_tracker.get_value() / self.cycle_seconds)
        )

    # def stop_vector_clock(self):
    #     self.vector_clock.remove_updater(self.start_vector_clock)
    def stop_vector_clock(self):
        self.vector_clock.clear_updaters()

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
    
    def config_zoomed_vectors(self, vectors):
        for v in vectors:
            v.max_tip_length_to_length_ratio = .15
            v.max_width_to_length_ratio = 0.05
            v.thickness = 0.02
            
              
    def get_circles(self, vectors):
        circles = VGroup()
        for v in vectors:
            c = Circle(radius = v.get_length(), **self.circle_config)            
            c.center_func = v.get_start
            c.radius_func = v.get_length
            self.update_circle(c)
            # c.add_updater(self.update_circle)            
            circles.add(c)
        return circles

    def update_circle(self, circle):           
        circle.set_width(2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle
    
    def update_circle_width(self, circles):
        for c in circles:
            c.set_stroke(width = .1)

   

    # def reset_circ_width(self, circles):
    #     for c in circles:
    #         c.set_stroke(width=self.circle_config['stroke_width']) 

    
    def update_circles(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, c in zip(it.count(1), circles):
            c.width = 2 * c.radius
            c.move_to(c.center_func())
            # c.set_stroke(width=min(
            #     1 / np.sqrt(k),
            #     # mcsw / k,
            #     mcsw,
            # ))
        
            
        
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
                width = .15* self.drawn_path_stroke_width * interpolate(broken_path.start_width, broken_path.end_width, (1 - (b % 1)))
            subpath.set_stroke(width=width)

class FourierScene(FourierSceneAbstract):
    def __init__(self):
        super().__init__()
        self.max_circle_stroke_width = 1

    def get_tex_symbol(self, symbol, color = None):
        symbol = Tex(symbol, **self.fourier_symbol_config)
    
        if (color is not None):
            symbol.set_color(color)

        return symbol

    def get_path_from_symbol(self, symbol):
        return symbol.family_members_with_points()[0]
    
    def make_decreasing_stroke_setter(alph):
        def inner(self, alph, circles):
            mcsw = self.max_circle_stroke_width
            for k, circle in zip(it.count(1), circles):
                circle.set_stroke(width=min(
                    alph * mcsw / np.sqrt(k),
                    # mcsw / k,
                    mcsw,
                ))
            return circles
        return  inner

    def construct(self):
        # Symbols to draw
        symbol1 = self.get_tex_symbol("m", RED)        
        group = VGroup(symbol1).arrange(RIGHT)

        # Fourier series for symbol1
        vectors1 = self.get_fourier_vectors(self.get_path_from_symbol(symbol1))
        circles1 = self.get_circles(vectors1)
        self.set_decreasing_stroke_widths(circles1)
        drawn_path1 = self.get_drawn_path(vectors1).set_color(RED)
        self.vectors = vectors1        

        # all_mobs = VGroup(group, text)
        all_mobs = VGroup(group)

        # Camera updater
        last_vector = vectors1[-1]

        def follow_end_vector(camera): 
                camera.move_to(center_of_mass([
                v.get_end()
                for v in self.vectors
        ]))

        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors1] #, vectors2]
                for arrow in vector_group
            ],
            # *[
            #     Create(circle)
            #     for circle_group in [circles1] #, circles2]
            #     for circle in circle_group
            # ],
            run_time=2.5,
        )

        # Add objects to scene
        self.add( 
            vectors1,
            circles1,
            drawn_path1.set_stroke(width = 0)            
        )

        # Camera move
        # self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)

        
        vectors1.add_updater(self.update_vectors)
        # circles1.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)

        # self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        # self.wait(1 * self.cycle_seconds)
        
        self.start_vector_clock()

        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        self.wait(.3 * self.cycle_seconds)
        
        self.stop_vector_clock()       
        # self.camera.frame.remove_updater(follow_end_vector)

        # vectors1.add_updater(self.config_zoomed_vectors)
        self.play(self.camera.frame.animate.scale(0.3).move_to(center_of_mass([
                v.get_end()
                for v in self.vectors
        ])), run_time = 3)  
        
        self.camera.frame.add_updater(follow_end_vector)
        # self.slow_factor = .1 
        self.start_vector_clock()
        self.slow_factor_tracker.set_value(.5)

        self.play(self.slow_factor_tracker.animate.set_value(.3), run_time = 0.5 * self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        # Move camera then write text
        self.camera.frame.remove_updater(follow_end_vector)
        self.play(
            self.camera.frame.animate.set_width(all_mobs.width * 1.5).move_to(all_mobs.get_center()))
        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.5 * self.cycle_seconds)
        
        # Remove updaters so can animate
        self.stop_vector_clock()
        
        for obj in [drawn_path1, vectors1, circles1]:
            obj.clear_updaters()
                
        self.play(
            *[
                Uncreate(vmobject)
                for vgroup in [vectors1, circles1] #vectors2, , circles2]
                for vmobject in vgroup
            ],
            FadeOut(drawn_path1), # drawn_path2),
            FadeIn(symbol1), # symbol2),
            run_time = 2.5,
        )

        self.wait(3)



class FourierFromSVG(FourierSceneAbstract):
    def __init__(self):
        super().__init__()
        self.file_name = "my_tulip_full_cycle"
        self.height = 6
        self.max_circle_stroke_width = 1
        self.circle_stroke_tracker = ValueTracker(1)
        self.vector_stroke_tracker = ValueTracker(1)



    
    def get_svg(self):
        shape = SVGMobject(self.file_name)
        return shape

    def get_path(self):
        shape = self.get_svg()
        path = shape.family_members_with_points()[0]
        # path.set_height(self.height)
        path.set_fill(opacity=0)
        path.set_stroke(WHITE, 0)
        return path
    
    # def make_decreasing_stroke_setter(self, alph):
    #     def inner(circles):
    #         mcsw = self.max_circle_stroke_width
    #         for k, circle in zip(it.count(1), circles):
    #             circle.set_stroke(width=min(
    #                 alph * mcsw / np.sqrt(k),
    #                 # mcsw / k,
    #                 mcsw,
    #             ))
    #         return circles
    #     return  inner
    
    def decreasing_stroke(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=min(
                self.circle_stroke_tracker.get_value()  / np.sqrt(k),
                # mcsw / k,
                mcsw,
            ))
        return circles
    
    def reset_vector_stroke(self, vectors):
        for v in vectors:            
            v.set_stroke(width=self.vector_stroke_tracker.get_value())


    def construct(self):
        # svg_mob = self.get_svg(self.file_name)
        # logo = Text("Филипенко Евгений\nrepetit-fm.ru", color=GRAY, font_size=12).to_corner(DR).shift(DOWN*.2)
        # logo.add_updater(lambda m: m.to_corner(DR).shift(DOWN *.2))
        
        scale_fac = 3.5
        inpath = self.get_path()
        inpath.scale(scale_fac)
        svgmob = self.get_svg().scale(scale_fac)
        vectors = self.get_fourier_vectors(inpath)
        circles = self.get_circles(vectors)
        # circles.add_updater(self.decreasing_stroke)
        self.decreasing_stroke(circles)
        drawn_path1 = self.get_drawn_path(vectors).set_color(GREEN)
        self.vectors = vectors
        
        all_mobs = VGroup(inpath, svgmob)

        # Camera updater
        last_vector = vectors[-1]

        def follow_end_vector(camera): 
                        camera.move_to(center_of_mass([
                        v.get_end()
                        for v in self.vectors
                ]))

        
        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors] #, vectors2]
                for arrow in vector_group
            ],
            *[
                Create(circle)
                for circle_group in [circles] #, circles2]
                for circle in circle_group
            ],
            run_time=2.5,
        )

        # Add objects to scene
        self.add( 
            vectors,
            circles,
            drawn_path1.set_stroke(width = 3),
            # logo            
        )

          # Camera move
        # self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)
        circles.add_updater(self.update_circles)        
        vectors.add_updater(self.update_vectors)
        
        # circles.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        

        # self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        # self.wait(1 * self.cycle_seconds)

        
        # Add updaters and start vector clock        
  
        self.start_vector_clock()
        self.slow_factor_tracker.set_value(.6)
        self.play(self.slow_factor_tracker.animate.set_value(.6), run_time = 0.6 * self.cycle_seconds)
        self.wait(.5 * self.cycle_seconds)
        
        self.stop_vector_clock()       
        # self.camera.frame.remove_updater(follow_end_vector)
        
        # vectors.add_updater(self.config_zoomed_vectors)
        circles.add_updater(self.decreasing_stroke)
        vectors.add_updater(self.reset_vector_stroke)
        # circles.remove_updater(self.update_circles)
        self.play(
            self.camera.frame.animate.scale(0.1).move_to(
                center_of_mass([
                v.get_end()
                for v in self.vectors
                ])),
                self.circle_stroke_tracker.animate.set_value(.2),
                self.vector_stroke_tracker.animate.set_value(.1),
                run_time = 3)
                
        self.camera.frame.add_updater(follow_end_vector)
        circles.remove_updater(self.decreasing_stroke)
        vectors.remove_updater(self.reset_vector_stroke)
        # self.make_decreasing_stroke_setter(.4)(circles)
        # circles.add_updater(self.set_decreasing_stroke_widths)
        # circles.add_updater(self.update_circles)
        
        # self.update_self(0) 
        # circles.add_updater(self.update_circles)
        # circles.add_updater(self.update_circle_width)
        # self.slow_factor = .1 
       
        self.start_vector_clock()
        self.slow_factor_tracker.set_value(.1)

        self.play(self.slow_factor_tracker.animate.set_value(.1), run_time = 1 * self.cycle_seconds)
        self.wait(1.3 * self.cycle_seconds)

        # # Move camera then write text
        # self.camera.frame.remove_updater(follow_end_vector)
        # # circles.remove_updater(self.update_circle_width)
        # circles.add_updater(self.decreasing_stroke)
        # vectors.add_updater(self.reset_vector_stroke)
        # self.play(
        #     self.camera.frame.animate.set_height(all_mobs.height * 1.2).move_to(all_mobs.get_center()),
        #     self.circle_stroke_tracker.animate.set_value(1),
        #     self.vector_stroke_tracker.animate.set_value(1))
        # circles.remove_updater(self.decreasing_stroke)
        # # self.make_decreasing_stroke_setter(1)(circles)
        # self.wait(0.3 * self.cycle_seconds)
        # self.play(self.slow_factor_tracker.animate.set_value(0), run_time = .7 * self.cycle_seconds)
        
        # # Remove updaters so can animate
        # self.stop_vector_clock()
        
        # for obj in [drawn_path1, vectors, circles]:
        #     obj.clear_updaters()
        # # for obj in [drawn_path2, vectors2, circles2]:
        # #     obj.clear_updaters()
        
        # self.play(
        #     *[
        #         Uncreate(vmobject)
        #         for vgroup in [vectors, circles] #vectors2, , circles2]
        #         for vmobject in vgroup
        #     ],
        #     FadeOut(drawn_path1), # drawn_path2),
        #     FadeIn(svgmob), # symbol2),
        #     run_time = 2.5,
        # )

        # # self.wait(1)
        # # self.play(ShowPassingFlash(svgmob.copy().set_color(YELLOW), run_time=3, time_width=.1))

        # self.wait(3)


class MyFourierOfPiSymbol(FourierScene):
    
    def __init__(self):
        super().__init__()
        self.fourier_symbol_config = {
            "stroke_width": 1,
            "fill_opacity": 1,
            "height": 4,
        }
        self.n_vectors = 101
        self.center_point = ORIGIN
        self.slow_factor = 0.1
        self.n_cycles = 1
        self.tex = r"\pi"
        self.start_drawn = False
        self.max_circle_stroke_width = 1    

    def add_vectors_circles_path(self):
        path = self.get_path()
        vectors = self.get_fourier_vectors(path)
        vectors.add_updater(self.update_vectors)        
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        # approx_path = self.get_vector_sum_path(circles)
        drawn_path = self.get_drawn_path(vectors).set_color(YELLOW)
        drawn_path.add_updater(self.update_path)
        if self.start_drawn:
            self.vector_clock.increment_value(1)

        # self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

    def run_one_cycle(self):        
        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.6 * self.cycle_seconds)
        time = 1 / self.slow_factor
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=min(
                # mcsw / np.sqrt(k),
                mcsw / k,
                mcsw,
            ))
        return circles

    def get_path(self):
        tex_mob = MathTex(self.tex)
        tex_mob.set_height(6)
        path = tex_mob.family_members_with_points()[0]
        path.set_fill(opacity=0)
        path.set_stroke(WHITE, 1)
        return path

    def construct(self):

        self.add_vectors_circles_path()        
        self.start_vector_clock()        
        self.run_one_cycle()

