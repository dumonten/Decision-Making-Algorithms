from tkinter import *
from PIL import Image, ImageTk
from neuralNetwork import *
from tkinter import filedialog

SCREEN_HEIGHT = 750
SCREEN_WIDTH = 1000
IM_HEIGHT = 28
IM_WIDTH = 28
BORDER = 5

BUTTONS_SIDE = LEFT
CANVAS_SIDE = RIGHT

BUTTON_WIDTH = 50
BUTTON_HEIGHT = 3

BORDER_COLOR = "white"
BACKGROUND_COLOR = "grey"
BUTTON_COLOR = "pink"
CANVAS_COLOR = "pink"
BRUSH_SIZE = 35
FONT = "Calibri 10"

input_nodes = 784
hidden_nodes = 200
output_nodes = 10
learning_rate = 0.1


class PaintApp(Tk):
    def __init__(self):
        super().__init__()

        # window properties
        self.title('LAB_9')
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y = (screen_height / 2) - (SCREEN_HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y - 30))

        # canvas properties
        self.canvas_frame = Frame(highlightbackground=BORDER_COLOR, highlightthickness=BORDER, relief=SOLID)
        self.canvas_frame.configure(background=BACKGROUND_COLOR)
        self.canvas_frame.pack(anchor="n", side=CANVAS_SIDE, fill=Y, padx=5)

        self.canvas_width = int(SCREEN_WIDTH // 1.5)
        self.canvas_height = SCREEN_HEIGHT
        self.brush_size = BRUSH_SIZE
        self.brush_color = "black"

        self.canvas = Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, bg=CANVAS_COLOR)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw)

        # app properties
        self.value = StringVar(value="")
        self.nn = NeuralNetwork.load(NeuralNetwork.get_load_file_name(input_nodes,
                                                                     hidden_nodes,
                                                                     output_nodes,
                                                                     learning_rate))
        # toolbar
        self.setup_toolbar()

    def save_canvas(self):
        fileName = "./image/drawing"
        self.canvas.postscript(file=fileName + '.eps')
        img = Image.open(fileName + '.eps')
        img = img.resize((IM_WIDTH, IM_HEIGHT))
        img.save(fileName + '.png', 'png')
        value = str(self.nn.query_image(fileName + '.png'))
        self.value.set(value)

    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.value.set("")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=(("PNG files", "*.png"), ))
        if file_path:
            img = Image.open(file_path)
            img = img.resize((self.canvas_width, self.canvas_height))
            img.show()
            self.clear_canvas()
            value = str(self.nn.query_image(file_path))
            self.value.set(value)

    def setup_toolbar(self):
        toolbar = Frame(highlightbackground=BORDER_COLOR, highlightthickness=BORDER, relief=SOLID)
        toolbar.configure(background=BACKGROUND_COLOR)
        toolbar.pack(anchor="n", side=BUTTONS_SIDE, fill=BOTH, expand=True, padx=5)

        label = Label(toolbar, text="Значение данной цифры:", font=FONT)
        label.pack(anchor="n", pady=20, padx=5)

        entry = Entry(toolbar, textvariable=self.value, font=FONT)
        entry.pack(anchor="n", pady=20, padx=5)

        save_button = Button(toolbar, text="Сохранить и классифицировать изображение", command=self.save_canvas, font=FONT, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        save_button.pack(anchor="n", pady=20, padx=5)
        save_button.configure(background=BUTTON_COLOR)

        open_file_button = Button(toolbar, text="Открыть изображение", command=self.browse_file, font=FONT, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        open_file_button.pack(anchor="n", pady=20, padx=5)
        open_file_button.configure(background=BUTTON_COLOR)

        clear_button = Button(toolbar, text="Очистить экран", command=self.clear_canvas, font=FONT, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        clear_button.pack(anchor="n", pady=20, padx=5)
        clear_button.configure(background=BUTTON_COLOR)


if __name__ == "__main__":
    paint_app = PaintApp()
    paint_app.mainloop()