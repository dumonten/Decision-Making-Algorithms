from tkinter import messagebox

from numpy import random
from tkinter import *
import graph

# '#RRGGBB'` или `'#RGB'`.
BACKGROUND_COLOR = "grey"
RAND_MAX = 1
RAND_MIN = 0


class Table:
    def _on_entry_change(self, i, j, *args):
        value = self.values[i][j].get()
        self.values[j][i].set(value)

    def __init__(self, root, num):
        self.values = [[StringVar(value="") for _ in range(num + 1)] for __ in range(num + 1)]

        self.frame = Frame(master=root, borderwidth=1, relief=SOLID)
        self.frame.pack(side="top", expand=True, fill=BOTH, pady=5, padx=5)

        self.vscrollbar = Scrollbar(self.frame, orient="vertical")
        self.vscrollbar.pack(side="right", fill="y")

        self.hscrollbar = Scrollbar(self.frame, orient="horizontal")
        self. hscrollbar.pack(side="bottom", fill="x")

        self.canvas = Canvas(self.frame, yscrollcommand=self.vscrollbar.set, xscrollcommand=self.hscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.vscrollbar.configure(command=self.canvas.yview)
        self.hscrollbar.configure(command=self.canvas.xview)

        self.scrollable_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.entries = []
        self.num = num
        for i in range(num + 1):
            self.entries.append([])
            for j in range(num + 1):
                e = Entry(self.scrollable_frame, width=10, font=('Times', 12), textvariable=self.values[i][j])
                self.entries[i].append(e)
                e.grid(row=i, column=j)
                if i == 0:
                    if j == 0:
                        self.values[i][j].set("")
                    else:
                        self.values[i][j].set(str(j))
                    e.configure(state='disabled')
                elif j == 0:
                    self.values[i][j].set(str(i))
                    e.configure(state='disabled')
                else:
                    if i == j:
                        e.configure(state='disabled')
                    e.configure(background=BACKGROUND_COLOR)
                    self.values[i][j].set("0")
                self.values[i][j].trace("w", lambda *args, i=i, j=j:
                self._on_entry_change(i, j, *args))
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def tbl_destroy(self):
        for i in range(self.num + 1): # а вот тут его удаляем
            for j in range(self.num + 1):
                self.entries[i][j].destroy()
            self.values[i].clear()
            self.entries[i].clear()
        self.entries.clear()
        self.values.clear()
        self.frame.destroy()
        self.scrollable_frame.destroy()
        self.vscrollbar.destroy()
        self.hscrollbar.destroy()
        self.canvas.destroy()

    def tbl_random(self):
        def set_entry_value(e, new_value):
            e.delete(0, END)
            e.insert(0, new_value)

        for i in range(1, self.num + 1):
            for j in range(i, self.num + 1):
                if i == j:
                    continue
                value = random.uniform(RAND_MIN, RAND_MAX)
                set_entry_value(self.entries[i][j], str(round(value, 2)))
                set_entry_value(self.entries[j][i], str(round(value, 2)))

    def tbl_get_graph(self):
        g = [{} for _ in range(self.num)]
        for i in range(1, self.num + 1):
            for j in range(i, self.num + 1):
                if i == j or self.entries[i][j].get() == 1e-10:
                    continue
                try:
                    value = float(self.entries[i][j].get())
                except ValueError:
                    messagebox.showerror('Ошибка',
                                           'Где-то Вы ввели неверное значение!')
                    return None
                graph.g_add_node(g, i-1, j-1, value)
        return g