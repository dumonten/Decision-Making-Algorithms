import PySimpleGUI as sg

layout_right = [
    [sg.Text("Количество терминальных цепочек", background_color="gray")],
    [sg.Slider(range=(7, 15), orientation="horizontal", background_color="gray", enable_events=True, key="-TERMINAL-")],
    [sg.Text("Предел длины терминальных цепочек", background_color="gray")],
    [sg.Slider(range=(5, 20), orientation="horizontal", background_color="gray", enable_events=True, key="-LEN-")],
    [sg.Button(button_text="Сгенерировать грамматику", size=(12, 4), button_color="gray", enable_events=True, key='-GRAMMAR-'),
     sg.Button(button_text="Сгенерировать набор слов по грамматике", button_color="gray", size=(12, 4), enable_events=True, key="-WORDS-")],
]

layout_center_right = [
    [sg.Text("Терминальные цепочки", background_color="gray")],
    [sg.Multiline(size=(30, 20), disabled=True, key='-T-', sbar_background_color="gray")],
]

layout_center_left = [
    [sg.Text("Грамматика", background_color="gray")],
    [sg.Multiline(size=(30, 20), disabled=True, key='-G-', sbar_background_color="gray")],
]

layout_left = [
    [sg.Text("Сгенерированные слова", background_color="gray")],
    [sg.Multiline(size=(30, 20), disabled=True, key='-W-', sbar_background_color="gray")],
]

layout = [
    [sg.Column(layout_left, background_color="gray"),
     sg.VerticalSeparator(),
     sg.Column(layout_center_left, background_color="gray"),
     sg.VerticalSeparator(),
     sg.Column(layout_center_right, background_color="gray")],
    [sg.Column(layout_right, background_color="gray")],
]
