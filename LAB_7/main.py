import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
from grammar import Grammar
from gui import layout
from tkinter import messagebox


def draw_figure(canvas, figure):
    tk_canvas = FigureCanvasTkAgg(figure, canvas)
    tk_canvas.draw()
    tk_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return tk_canvas


matplotlib.use('TkAgg')
fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.clear()

window = sg.Window('MiAPR7', layout, finalize=True, element_justification='left', background_color='gray')

canvas = draw_figure(window['-CV-'].TKCanvas, fig)

grammar = Grammar(rand_c=False)
grammar.draw(ax)
canvas.draw()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-GEN-':
        ax.clear()
        grammar = Grammar(rand_c=False)
        grammar.draw(ax)
        canvas.draw()
    if event == '-BGEN-':
        ax.clear()
        grammar = Grammar(rand_c=True)
        grammar.draw(ax)
        canvas.draw()
    if event == '-RULE-':
        if grammar.check_rules():
            messagebox.showinfo("Ошибка",
                                "Изображение соответствует правилам грамматики")
        else:
            messagebox.showerror("Ошибка",
                                 "Изображение не соответствует правилам грамматики")
