import PySimpleGUI as sg
from gui import layout
from logic import generate_words, get_grammar, \
    words_to_string, grammar_to_string, generate_example_words

window = sg.Window(title='LAB8', layout=layout, finalize=True, background_color="gray", element_justification='center')

word_set, added_set = generate_words(7, 5)
if len(added_set) != 0:
    window["-T-"].update(words_to_string(word_set) + "\n Добавленные окончания \n" + words_to_string(added_set))
else:
    window["-T-"].update(words_to_string(word_set))
word_set.extend(added_set)
grammar = get_grammar(word_set)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event in ("-TERMINAL-", "-LEN-"):
        word_set, added_set = generate_words(int(values["-TERMINAL-"]), int(values["-LEN-"]))
        if len(added_set) != 0:
            window["-T-"].update(words_to_string(word_set) + "\n Добавленные окончания \n" + words_to_string(added_set))
        else:
            window["-T-"].update(words_to_string(word_set))
        word_set.extend(added_set)
        grammar = get_grammar(word_set)
        window["-G-"].update("")
        window["-W-"].update("")
    if event == "-GRAMMAR-":
        window["-G-"].update(grammar_to_string(grammar))
        window["-W-"].update("")
    if event == "-WORDS-":
        window["-W-"].update(generate_example_words(grammar, 10))
