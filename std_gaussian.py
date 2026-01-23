from manim import *
from math import sin
import math
import numpy as np


class GraphExample(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(1)
        self.camera.background_color = "#0f0f14"


        axes = Axes(x_range=[-5, 5, 0.4], y_range=[0, 2, 1], axis_config={
            "include_numbers": False,
            "include_ticks": False
        })
        labels = axes.get_axis_labels(x_label="x", y_label=MathTex("p(x)"))

        sigma_tracker = ValueTracker(0.4)
        std_mult = ValueTracker(1)

        def f(x):
            s = sigma_tracker.get_value()

            return (1 / (s * math.sqrt(2 * math.pi))) * math.exp((-(x-0) ** 2) / (2 * s ** 2))


        def area_between(a, b, n = 1000):
            xs = np.linspace(a, b, n)
            ys = [f(x) for x in xs]
            return np.trapz(ys, xs)

        value = DecimalNumber(0, num_decimal_places=2)
        value.add_updater(
                lambda d: d.set_value(
                    area_between(0 - sigma_tracker.get_value() * std_mult.get_value(),
                                 0 + sigma_tracker.get_value() * std_mult.get_value())* 100
                )
        )


        value.shift(RIGHT * 2)
        

        g = always_redraw(lambda: axes.plot(f, color=RED))

        area = always_redraw(
                lambda: axes.get_area(
                    g,
                    x_range=[0 - sigma_tracker.get_value() * std_mult.get_value(),
                             0 + sigma_tracker.get_value() * std_mult.get_value()],
                    color=[BLUE, GREEN],
                    opacity=0.4
                    
                )
            )

        left_line = always_redraw(
            lambda: axes.get_vertical_line(
                axes.c2p(
                    -sigma_tracker.get_value() * std_mult.get_value(),
                    0
                ),
                color=YELLOW
            )
        )

        right_line = always_redraw(
            lambda: axes.get_vertical_line(
                axes.c2p(
                    sigma_tracker.get_value() * std_mult.get_value(),
                    0
                ),
                color=YELLOW
            )
        )

        label_left = always_redraw(
            lambda: MathTex(
                f"-{std_mult.get_value():.0f}\\sigma"
            ).next_to(left_line, DOWN)
        )

        label_right = always_redraw(
            lambda: MathTex(
                f"+{std_mult.get_value():.0f}\\sigma"
            ).next_to(right_line, DOWN)
        )

        formula = MathTex(
            r"p(x)=\frac{1}{\sigma\sqrt{2\pi}}",
            r"\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)",
            font_size=36
        ).to_corner(UL)




        self.play(Write(axes), Write(labels))
        self.play(Write(formula), run_time=2)
        self.play(Write(g), run_time=4)
        self.play(AnimationGroup(FadeIn(area), Write(value), AnimationGroup(Create(left_line),Create(label_left), Create(right_line),Create(label_right))), run_time=4)

        self.play(self.camera.frame.animate.move_to(axes.c2p(0,0)).scale(0.8), run_time=6)
        self.play(sigma_tracker.animate.set_value(1.2), run_time=4)
        self.wait(1)
        self.play(std_mult.animate.set_value(2), run_time = 4)
        

        self.wait(3)

        self.play(self.camera.frame.animate.scale(1.3).move_to(ORIGIN))

        self.play(sigma_tracker.animate.set_value(0.7), run_time=4)

        self.wait(2)

        self.play(std_mult.animate.set_value(3), run_time = 4)

        self.wait(2)