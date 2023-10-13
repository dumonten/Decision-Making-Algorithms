from tkinter import *
from tkinter import scrolledtext, messagebox

import numpy as np

from potential_classifier import *
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
NUM_OF_ATTRIBUTES = 2
NUM_OF_POINTS_FOR_PLOT = 10000


class App(Tk):

    def __init__(self):
        super().__init__()
        self.title('LAB_5')
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y = (screen_height / 2) - (SCREEN_HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y - 30))

        self.potential_classifier = None
        self.num_vectors = IntVar(value=2)
        self.num_attributes = IntVar(value=NUM_OF_ATTRIBUTES)
        self.entry_function = StringVar(value="")
        self.entry_object_attributes = StringVar(value="")
        self.entry_find_class = IntVar(value=0)
        self.label_for_object_class_search = \
            StringVar(value=f"Пожалуйста, введите координаты (x, y) точки (объекта)")
        self.function = np.array([], dtype=np.int64)

        self._init_controls()

    def _init_controls(self):
        frame = Frame(borderwidth=1, relief=SOLID)
        self._init_sliders_area(master=frame)
        self._init_find_class_area(master=frame)
        frame.pack(anchor="n", side="top", fill=X, padx=5)
        self._init_plot_area()

    def _init_plot_area(self):
        frame = Frame(borderwidth=1, relief=SOLID, padx=10, pady=5)
        self.figure = plt.Figure(dpi=70)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

        label_1 = Label(frame, text="Разделяющая функция", font="Times 12")
        entry_function = Entry(frame, textvariable=self.entry_function, state=DISABLED)
        label_1.pack(anchor="n")
        entry_function.pack(anchor="n", fill=X)

        frame.pack(anchor="se", fill=X, padx=5, pady=5)

    def _init_sliders_area(self, master):
        def _on_click():
            self.potential_classifier = PotentialClassifier(self.num_vectors.get(),
                                                            self.num_attributes.get())
            self._set_text_to_entry_training_set()

            limit_is_reached = self.potential_classifier.get_function()
            if limit_is_reached:
                messagebox.showwarning('Предупреждение',
                                       'Превышено число итераций! Допускается неверная классификация.')
            self.function = self.potential_classifier.function
            self.entry_function.set(self.potential_classifier.function_to_string())
            self._draw_plots()

        def _slider_classes_num_on_change(event):
            pass

        frame = Frame(master=master, borderwidth=1, relief=SOLID)
        slider_num_vectors = Scale(frame,
                                   variable=self.num_vectors,
                                   from_=4,
                                   to=6,
                                   resolution=2,
                                   orient=HORIZONTAL,
                                   command=_slider_classes_num_on_change, font="Times 10")

        label_1 = Label(frame, text="Количество объектов в двух классах", font="Times 10")
        label_1.pack(anchor="n")
        slider_num_vectors.pack(anchor="n", fill=X)

        self.entry_training_set = scrolledtext.ScrolledText(frame,
                                                            font="Times 10",
                                                            height=10,
                                                            width=10,
                                                            state=DISABLED
                                                            )
        self.entry_training_set.pack(anchor="n", pady=5, fill=X)
        button = Button(frame, text="Произвести расчет классифицирующей функции", command=_on_click)
        button.pack(anchor="center", side="bottom", pady=5)
        frame.pack(anchor="nw", side="left", expand=True, fill=X, pady=5, padx=5)

    def _set_text_to_entry_training_set(self):
        self.entry_training_set.config(state=NORMAL)
        self.entry_training_set.delete('1.0', END)
        self.entry_training_set.insert(INSERT, self.potential_classifier.training_set_to_string())
        self.entry_training_set.config(state=DISABLED)

    def _init_find_class_area(self, master):
        def _on_click():
            if self.potential_classifier is None:
                messagebox.showerror('Ошибка', 'Вы не создали обучающую выборку!')
                return
            try:
                _ = self.entry_object_attributes.get()
                vector = np.array(list(map(int, _.split(", "))))
            except Exception:
                messagebox.showerror('Ошибка', 'Вы ввели некорректные данные!')
                return
            cls_id = self.potential_classifier.classify(vector, self.function)
            self.entry_find_class.set(cls_id)

        frame = Frame(master=master, borderwidth=1, relief=SOLID)
        label_1 = Label(frame, text="Класссифицировать объект", font="Times 12")
        label_2 = Label(frame,
                        font="Times 10",
                        textvariable=self.label_for_object_class_search)
        label_3 = Label(frame, text=f"Обнаруженный класс", font="Times 10")
        entry_object_attributes = Entry(frame, textvariable=self.entry_object_attributes)
        entry_class_num = Entry(frame, textvariable=self.entry_find_class, state=DISABLED)

        label_1.pack(anchor="n")
        label_2.pack(anchor="n")
        entry_object_attributes.pack(anchor="n", fill=X)
        button = Button(frame, text="Обнаружить класс", command=_on_click)
        button.pack(anchor="center", side="top", pady=5)
        label_3.pack(anchor="n")
        entry_class_num.pack(anchor="n", fill=X)
        frame.pack(anchor="ne", side="right", expand=True, fill=BOTH, pady=5, padx=5)

    def _draw_plots(self):
        self.ax.clear()
        training_set = self.potential_classifier.training_set

        # generate points
        cls_0_points_x = [vector[0] for vector in
                          training_set[:len(training_set) // 2]]
        cls_0_points_y = [vector[1] for vector in
                          training_set[:len(training_set) // 2]]
        self.ax.scatter(cls_0_points_x, cls_0_points_y, s=40, color='black')

        cls_1_points_x = [vector[0] for vector in
                          training_set[len(training_set) // 2:]]
        cls_1_points_y = [vector[1] for vector in
                          training_set[len(training_set) // 2:]]
        self.ax.scatter(cls_1_points_x, cls_1_points_y, s=40, color='red')

        # draw plots
        x = np.linspace(-10, 10, NUM_OF_POINTS_FOR_PLOT)
        y = (self.function[3] * x + self.function[2])
        if all(y) != 0:
            y = -1 * (self.function[1] * x + self.function[0]) / y
        else:
            y = np.linspace(0, 0, NUM_OF_POINTS_FOR_PLOT)

        # Построение графика
        self.ax.scatter(x, y, color='b', s=2, label=self.entry_function.get())
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.legend()

        self.ax.grid(color='black', linewidth=0.5)

        self.ax.set_xticks([x for x in range(-15, 15)])
        self.ax.set_ylim([-15, 15])
        self.canvas.draw()


if __name__ == '__main__':
    app = App()
    app.mainloop()
