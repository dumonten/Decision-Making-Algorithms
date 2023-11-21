import copy
import math
from tkinter import *
from tkinter import scrolledtext, messagebox
from table import *
import numpy as np
import graph
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
NUM_OF_ATTRIBUTES = 2
NUM_OF_POINTS_FOR_PLOT = 10000

BACKGROUND_COLOR = "grey"
GRAPH_COLOR = "black"
BORDER = 2
FONT = "Calibri 12"


class App(Tk):

    def __init__(self):
        super().__init__()

        # app window properties
        self.title('LAB_6')
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y = (screen_height / 2) - (SCREEN_HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y - 30))

        # app functional properties
        self.element_quantity = IntVar(value=0)
        self.table = None

        # init window elements
        self._init_controls()

    def _init_controls(self):
        frame = Frame(borderwidth=BORDER, relief=SOLID)
        self._init_table_area(master=frame)
        self._init_buttons_area(master=frame)
        frame.configure(background=BACKGROUND_COLOR)
        frame.pack(anchor="n", side="left", fill=Y, padx=5)
        self._init_plot_area()

    def _init_plot_area(self):
        frame = Frame(borderwidth=BORDER, relief=SOLID, padx=10, pady=5)
        self.figure = plt.Figure(dpi=70)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

    def _init_table_area(self, master):
        def _on_click_random():
            self.table.tbl_random()

        def _slider_classes_num_on_change(event):
            self.table.tbl_destroy()
            self.table = Table(frame, self.element_quantity.get())

        frame = Frame(master=master, borderwidth=BORDER, relief=SOLID)

        # slider label button
        slider_num_vectors = Scale(frame,
                                   variable=self.element_quantity,
                                   from_=2,
                                   to=15,
                                   resolution=1,
                                   orient=HORIZONTAL,
                                   command=_slider_classes_num_on_change, font=FONT)
        label_1 = Label(frame, text="Количество элементов", font=FONT)
        button = Button(frame, text="Заполнить рандомными значениями", command=_on_click_random)

        label_1.pack(anchor="n")
        slider_num_vectors.pack(anchor="n", fill=X)
        button.pack(anchor="n", pady=5)

        # table
        self.table = Table(frame, self.element_quantity.get())
        frame.pack(side="top", expand=True, fill=BOTH, pady=5, padx=5)

    def _init_buttons_area(self, master):
        def _on_click_max():
            g = self.table.tbl_get_graph()
            if g is not None:
                tree = graph.g_get_tree(g, 'max')
                self._draw_plots(tree)

        def _on_click_min():
            g = self.table.tbl_get_graph()
            if g is not None:
                tree = graph.g_get_tree(g, 'min')
                self._draw_plots(tree)

        frame = Frame(master=master, borderwidth=BORDER, relief=SOLID)

        label_1 = Label(frame, text="Критерий классификации", font=FONT)
        label_1.pack(anchor="n")

        button_max = Button(frame, text="Макисимум", height=5, width=30, command=_on_click_max)
        button_min = Button(frame, text="Минимум", height=5, width=30, command=_on_click_min)

        button_max.configure(background=BACKGROUND_COLOR)
        button_min.configure(background=BACKGROUND_COLOR)
        button_max.pack(anchor="center", side="top", pady=5)
        button_min.pack(anchor="center", side="top", pady=5)

        frame.pack(side="top", fill=BOTH, pady=5, padx=5)

    def _draw_plots(self, tree):
        self.ax.clear()

        num = self.element_quantity.get()
        offset = 1
        x, y = [0] * num, [0] * num

        xtick_labels = []
        xtick = []

        max_y = -math.inf

        for idx, elem in enumerate(tree):
            if x[elem[0]] == 0:
                x[elem[0]] = offset * 10
                offset += 1
                xtick_labels.append(f'x{elem[0] + 1}')
                xtick.append(x[elem[0]])
            if x[elem[1]] == 0:
                x[elem[1]] = offset * 10
                offset += 1
                xtick_labels.append(f'x{elem[1] + 1}')
                xtick.append(x[elem[1]])
            self.ax.vlines(x=x[elem[0]], ymin=y[elem[0]], ymax=elem[2], colors=GRAPH_COLOR)
            self.ax.vlines(x=x[elem[1]], ymin=y[elem[1]], ymax=elem[2], colors=GRAPH_COLOR)
            self.ax.hlines(y=elem[2], xmin=x[elem[0]], xmax=x[elem[1]], colors=GRAPH_COLOR)
            self.ax.scatter([x[elem[0]], x[elem[1]]], [y[elem[0]], y[elem[1]]], s=20)

            x[elem[0]] = abs(x[elem[1]] + x[elem[0]]) // 2
            y[elem[0]] = elem[2]

            if max_y < elem[2]:
                max_y = elem[2]

            if idx == len(tree) - 1:
                self.ax.scatter([x[elem[0]]], [y[elem[0]]], color='black', s=20)
        self.ax.grid(color='black', linewidth=0.5)

        self.ax.set_xticks(xtick)
        self.ax.set_xticklabels(xtick_labels)

        self.ax.set_ylim([0, max_y + 0.2])
        self.ax.set_yticks(np.linspace(0, max_y + 0.2, 20))
        self.canvas.draw()


if __name__ == '__main__':
    app = App()
    app.mainloop()
