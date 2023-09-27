from tkinter import *
from tkinter import scrolledtext, messagebox
from perceptron import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750


class App(Tk):

    def __init__(self):
        super().__init__()
        self.title('LAB_3')
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y = (screen_height / 2) - (SCREEN_HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y - 30))

        self.perceptron = None
        self.classes_num = IntVar(value=1)
        self.objects_per_class_num = IntVar(value=1)
        self.attributes_num = IntVar(value=1)
        self.entry_object_attributes = StringVar(value="")
        self.entry_find_class = IntVar(value=0)
        self.label_for_oject_class_search = \
            StringVar(value=f"Пожалуйста, введите {self.attributes_num.get()} атрибут(ов) объекта")
        self.functions = []

        self._init_controls()

    def _init_controls(self):
        frame = Frame(borderwidth=1, relief=SOLID)
        self._init_sliders_area(master=frame)
        self._init_find_class_area(master=frame)
        frame.pack(anchor="n", side="top", fill=X, padx=5)
        self._init_edit_area()

    def _init_edit_area(self):
        frame = Frame(borderwidth=1, relief=SOLID)
        label_1 = Label(frame, text="Обучающая выборка", font="Times 12")
        self.entry_training_set = scrolledtext.ScrolledText(frame,
                                                            font="Times 12",
                                                            height=10,
                                                            state=DISABLED
                                                            )
        label_1.pack(anchor="n")
        self.entry_training_set.pack(anchor="n", pady=5, fill=X)
        frame.pack(anchor="s", side="top", fill=X, padx=5, pady=10)

        frame = Frame(borderwidth=1, relief=SOLID)
        label_1 = Label(frame,
                        text="Решающие функции",
                        font="Times 12"
                        )
        self.entry_functions = scrolledtext.ScrolledText(frame,
                                                         font="Times 12",
                                                         height=10,
                                                         state=DISABLED
                                                         )
        label_1.pack(anchor="n")
        self.entry_functions.pack(anchor="n", pady=5, fill=X)
        frame.pack(anchor="n", side="top", fill=X, padx=5, pady=10)

    def _init_sliders_area(self, master):
        def _on_click():
            self.perceptron = Perceptron(self.classes_num.get(),
                                         self.objects_per_class_num.get(),
                                         self.attributes_num.get())
            self.perceptron.generate_random_classes()
            functions = self.perceptron.get_decision_functions()

            self.entry_training_set.config(state=NORMAL)
            self.entry_functions.config(state=NORMAL)
            self.entry_training_set.delete('1.0', END)
            self.entry_functions.delete('1.0', END)
            self.entry_training_set.insert(INSERT, self.perceptron.classes_to_string())
            self.entry_functions.insert(INSERT, Perceptron.functions_to_string(self.perceptron.classes_num, functions))
            self.entry_training_set.config(state=DISABLED)
            self.entry_functions.config(state=DISABLED)

        def _slider_classes_num_on_change(event):
            pass

        def _slider_objects_per_class_num_on_change(event):
            pass

        def _slider_attributes_num(event):
            self.label_for_oject_class_search.set(
                f"Пожалуйста, введите {self.attributes_num.get()} атрибут(ов) объекта")

        frame = Frame(master=master, borderwidth=1, relief=SOLID)

        slider_classes_num = Scale(frame,
                                   variable=self.classes_num,
                                   from_=1,
                                   to=10,
                                   orient=HORIZONTAL,
                                   command=_slider_classes_num_on_change, font="Times 10")
        slider_objects_per_class_num = Scale(frame,
                                             variable=self.objects_per_class_num,
                                             from_=1,
                                             to=100,
                                             orient=HORIZONTAL,
                                             command=_slider_objects_per_class_num_on_change, font="Times 10")
        slider_attributes_num = Scale(frame,
                                      variable=self.attributes_num,
                                      from_=1,
                                      to=100,
                                      orient=HORIZONTAL,
                                      command=_slider_attributes_num, font="Times 10")

        label_1 = Label(frame, text="Количество классов", font="Times 10")
        label_2 = Label(frame, text="Количество объектов в каждом классе", font="Times 10")
        label_3 = Label(frame, text="Количество атрибутов каждого объекта", font="Times 10")

        label_1.pack(anchor="n")
        slider_classes_num.pack(anchor="n", fill=X)
        label_2.pack(anchor="n")
        slider_objects_per_class_num.pack(anchor="n", fill=X)
        label_3.pack(anchor="n")
        slider_attributes_num.pack(anchor="n", fill=X)

        button = Button(frame, text="Произвести расчет решающих функций", command=_on_click)
        button.pack(anchor="center", side="bottom", pady=5)
        frame.pack(anchor="nw", side="left", expand=True, fill=X, pady=5, padx=5)

    def _init_find_class_area(self, master):
        def _on_click():
            if self.perceptron is None:
                messagebox.showerror('Ошибка', 'Вы не создали обучающую выборку!')
                return
            pobject = PerceptronObject.set_data(self.entry_object_attributes.get(), self.perceptron.attributes_num)
            if pobject is None:
                messagebox.showerror('Ошибка', 'Вы ввели некорректные данные!')
                return
            self.entry_find_class.set(self.perceptron.get_class(pobject))

        frame = Frame(master=master, borderwidth=1, relief=SOLID)
        label_1 = Label(frame, text="Класссифицировать объект", font="Times 12")
        label_2 = Label(frame,
                        font="Times 10",
                        textvariable=self.label_for_oject_class_search)
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


if __name__ == '__main__':
    app = App()
    app.mainloop()
