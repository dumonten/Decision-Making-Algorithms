import PySimpleGUI as sg

layout_right = [
    [sg.Button(button_text="Генерирование изображения,\n соответствующее по грамматике", size=(35, 4), button_color=('white', 'gray'), enable_events=True, key='-GEN-')],
    [sg.Button(button_text="Генерирование изображения,\n НЕ соответствующее по грамматике", size=(35, 4), button_color=('white', 'gray'), enable_events=True, key='-BGEN-')],
    [sg.Button(button_text="Проверить на соответствие правил грамматики", size=(35, 4), button_color=('white', 'gray'), enable_events=True, key="-RULE-")],
    [sg.Text("", enable_events=True, key="-O-", background_color='gray', text_color='white')],
]

layout_left = [
    [sg.Text('', background_color='gray', text_color='white')],
    [sg.Canvas(key='-CV-', background_color='gray')],
]

layout = [
    [sg.Column(layout_left, background_color='gray'),
     sg.VerticalSeparator(),
     sg.Column(layout_right, background_color='gray')],
]
