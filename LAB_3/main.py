import math
import random
from tkinter import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FONT = "Times 14"

NUM_OF_POINTS = 1000
LEFT_BOUND_1 = -100
RIGHT_BOUND_1 = 600
LEFT_BOUND_2 = 200
RIGHT_BOUND_2 = 1000
max_y_value = 0.002


def get_class(lbound, rbound, num):
    class_params = [0.0, 0.0]
    points = [0] * num
    for i in range(num):
        points[i] = random.randint(lbound, rbound)
        class_params[0] += points[i]
    class_params[0] /= num
    for i in range(num):
        class_params[1] += (points[i] - class_params[0]) ** 2
    class_params[1] = math.sqrt(class_params[1] / num)
    return class_params


def gauss_baes(x, mx, sigma, p):
    return np.exp(-0.5 * ((x - mx) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi)) * p


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('LAB_3')
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y = (screen_height / 2) - (SCREEN_HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y))

        self.slider_PC1_value = DoubleVar(value=0.5)
        self.slider_PC2_value = DoubleVar(value=0.5)
        self.false_alarm_prob = DoubleVar(value=0.0)
        self.miss_detect_prob = DoubleVar(value=0.0)
        self.sum_class_error = DoubleVar(value=0.0)

        self.C1 = get_class(LEFT_BOUND_1, RIGHT_BOUND_1, NUM_OF_POINTS)
        self.C2 = get_class(LEFT_BOUND_2, RIGHT_BOUND_2, NUM_OF_POINTS)

        self.x = [0] * NUM_OF_POINTS
        for i in range(NUM_OF_POINTS):
            self.x[i] = random.randint(min(LEFT_BOUND_1, LEFT_BOUND_2), max(RIGHT_BOUND_1, RIGHT_BOUND_2))
        self.x.sort()
        self._init_controls()

        frame = Frame(borderwidth=1, relief=SOLID, padx=10, pady=5)
        self.figure = plt.Figure(dpi=70)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xticks([x for x in range(min(self.x), max(self.x), 100)])
        self.ax.set_ylim([0.0, max_y_value])
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        frame.pack(anchor="se", fill=X, padx=5, pady=5)

    def _init_controls(self):
        self._init_sliders()

        frame = Frame(borderwidth=1, relief=SOLID, padx=10, pady=5)
        label_results = Label(frame, text="Результаты", font="Times 16")
        label_results.pack(anchor="sw")

        label_false_alarm_prob = Label(frame, text="Вероятность ложной тревоги", font="Times 12")
        entry = Entry(frame, textvariable=self.false_alarm_prob, state=DISABLED)
        label_false_alarm_prob.pack(anchor="sw")
        entry.pack(anchor="sw", fill=X)

        label_miss_detect_prob = Label(frame, text="Вероятность пропуска обнаружения", font="Times 12")
        entry = Entry(frame, textvariable=self.miss_detect_prob, state=DISABLED)
        label_miss_detect_prob.pack(anchor="sw")
        entry.pack(anchor="sw", fill=X)

        label_sum_class_error = Label(frame, text="Суммарная ошибка классификации", font="Times 12")
        entry = Entry(frame, textvariable=self.sum_class_error, state=DISABLED)
        label_sum_class_error.pack(anchor="sw")
        entry.pack(anchor="sw", fill=X)

        frame.pack(anchor="se", fill=X, padx=5, pady=5)

    def _init_sliders(self):
        def _slider_pc1_on_change(event):
            self.slider_PC2_value.set(1.0 - self.slider_PC1_value.get())
            self._draw_plots()

        def _slider_pc2_on_change(event):
            self.slider_PC1_value.set(1.0 - self.slider_PC2_value.get())
            self._draw_plots()

        frame = Frame(borderwidth=1, relief=SOLID, padx=10, pady=5)

        slider_PC1 = Scale(frame,
                           variable=self.slider_PC1_value,
                           from_=0.0,
                           to=1.0,
                           digits=4,
                           resolution=0.001,
                           orient=HORIZONTAL,
                           command=_slider_pc1_on_change, font="Times 12")
        slider_PC2 = Scale(frame,
                           variable=self.slider_PC2_value,
                           from_=0.0,
                           to=1.0,
                           digits=4,
                           resolution=0.001,
                           orient=HORIZONTAL,
                           command=_slider_pc2_on_change, font="Times 12")

        label_PC1 = Label(frame, text="P(C1)", font="Times 10")
        label_PC2 = Label(frame, text="P(C2)", font="Times 10")

        label_PC1.pack(anchor="sw")
        slider_PC1.pack(anchor="sw", fill=X)
        label_PC2.pack(anchor="sw")
        slider_PC2.pack(anchor="sw", fill=X)

        frame.pack(anchor="sw", fill=X, padx=5, pady=5)

    def _draw_plots(self):
        self.ax.clear()

        common_point, common_ind = math.inf, math.inf
        c1, c2 = [0]*len(self.x), [0]*len(self.x)
        for i, xi in enumerate(self.x):
            c1[i] = gauss_baes(xi, self.C1[0], self.C1[1], self.slider_PC1_value.get())
            c2[i] = gauss_baes(xi, self.C2[0], self.C2[1], self.slider_PC2_value.get())
            if np.abs(c1[i] - c2[i]) < common_point:
                common_point = np.abs(c1[i] - c2[i])
                common_ind = i

        _1 = np.sum([min(c11, c22) for c11, c22 in zip(c1[:int(common_ind)], c2[:int(common_ind)])])
        _2 = np.sum([min(c11, c22) for c11, c22 in zip(c1[int(common_ind):], c2[int(common_ind):])])
        _3 = _1 + _2

        self.false_alarm_prob.set(float(_1))
        self.miss_detect_prob.set(float(_2))
        self.sum_class_error.set(_3)

        # max_y_value = max(max(c1), max(c2))
        self.ax.set_xticks([x for x in range(min(self.x), max(self.x), 100)])
        self.ax.set_ylim([0.0, max_y_value])

        self.ax.plot(self.x, c1, linewidth=2, markersize=5, markerfacecolor='blue', label=r'$\ p(C1)*p(Xm/C1) $')
        # self.ax.scatter(self.x, c1, s=3, color='black')
        self.ax.plot(self.x, c2, linewidth=2, markersize=5, markerfacecolor='red', label=r'$\ p(C2)*p(Xm/C2) $')
        # self.ax.scatter(self.x, c2, s=3, color='black')
        self.ax.plot([self.x[common_ind],
                      self.x[common_ind]],
                     [0, max_y_value],
                     linewidth=2,
                     markerfacecolor='green',
                     label=r'$\ X* $')
        self.ax.grid(color='black', linewidth=0.5)
        self.ax.legend()
        self.canvas.draw()


if __name__ == '__main__':
    app = App()
    app.mainloop()
