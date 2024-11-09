
import tkinter as tk
from tkinter import Button, Canvas, filedialog, Label, Entry, colorchooser, ttk
from PIL import Image, ImageDraw
from core.MultiLayerPerceptron import MultiLayerPerceptron
from domain.ClassLabelMapping import ClassLabelMapping
from loss.CrossEntropyLossFunction import CrossEntropyLossFunction
from configuration.MultiLayerPerceptronConfiguration import MultiLayerPerceptronConfiguration
from util.MatrixCsvLoader import MatrixCsvLoader
import TKinterModernThemes as TKMT

GRID_SIZE = 32
PIXEL_SIZE = 15


class PixelArtApp(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Лабараторная_2 Левицкая.А.И", "azure", "dark")
        self.mlp = None
        self.input_size = 32 * 32
        self.hidden_layer_sizes = [128, 64]
        self.output_size = 10
        self.learning_rate = 0.2
        self.loss_function = CrossEntropyLossFunction()

        self.selected_color = "black"

        self.canvas = Canvas(self.root, width=GRID_SIZE * PIXEL_SIZE, height=GRID_SIZE * PIXEL_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.clear_button = self.Button(text="Очистить", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=0, padx=5, pady=5)

        self.save_button = self.Button(text="Сохранить", command=self.save_image)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.load_button = self.Button(text="Загрузить изображение", command=self.load_image)
        self.load_button.grid(row=1, column=2, padx=5, pady=5)

        self.color_button = self.Button(text="Выбрать цвет", command=self.choose_color)
        self.color_button.grid(row=1, column=3, padx=5, pady=5)

        self.epochs_label = self.Label(text="Количество эпох:")
        self.epochs_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.epochs = tk.StringVar(value="7")
        self.epochs_entry = self.Entry(self.epochs)
        self.epochs_entry.grid(row=2, column=1, padx=5, pady=5)

        self.lr_label = self.Label(text="Скорость обучения:")
        self.lr_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.lr = tk.StringVar(value="0.2")
        self.lr_entry = self.Entry(self.lr)
        self.lr_entry.grid(row=3, column=1, padx=5, pady=5)

        self.train_button = self.Button(text="Начать обучение", command=self.start_training)
        self.train_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.train_button = self.Button(text="Распознать", command=self.predict)
        self.train_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        self.pixels = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.drawing = False
        self.image = Image.new("1", (GRID_SIZE, GRID_SIZE), color=1)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_pixel)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.update_canvas()
        self.run()

    def start_draw(self, event):
        self.drawing = True
        self.toggle_pixel(event)

    def stop_draw(self, event):
        self.drawing = False

    def draw_pixel(self, event):
        if self.drawing:
            self.toggle_pixel(event)

    def toggle_pixel(self, event):
        x = event.x // PIXEL_SIZE
        y = event.y // PIXEL_SIZE

        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            self.pixels[y][x] = 1 - self.pixels[y][x]
            color = self.selected_color
            self.canvas.create_rectangle(x * PIXEL_SIZE, y * PIXEL_SIZE,
                                         (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                                         fill=color, outline="gray")

            self.draw.point((x, y), fill=color)

    def clear_canvas(self):
        self.pixels = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.image = Image.new("1", (GRID_SIZE, GRID_SIZE), color=1)
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = "white" if self.pixels[y][x] == 0 else "black"
                self.canvas.create_rectangle(x * PIXEL_SIZE, y * PIXEL_SIZE,
                                             (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                                             fill=color, outline="gray")

    def choose_color(self):
        # Открываем диалог выбора цвета
        color_code = colorchooser.askcolor(title="Выбрать цвет")
        if color_code:
            self.selected_color = color_code[1]

    def save_image(self):
        self.image.save("pixel_art.bmp")
        print("Изображение сохранено как pixel_art.bmp")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.bmp")])
        if file_path:
            image = Image.open(file_path).convert("1")
            image = image.resize((GRID_SIZE, GRID_SIZE))
            self.pixels = self.image_to_pixel_array(image)
            print(self.pixels)
            self.update_canvas()
            print("Изображение загружено и преобразовано в массив пикселей.")

    def image_to_pixel_array(self, image):
        pixel_array = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                pixel_value = image.getpixel((x, y))
                pixel_array[y][x] = 1.0 if pixel_value == 0 else 0.0
        return pixel_array

    def start_training(self):
        epochs = int(self.epochs_entry.get())
        learning_rate = float(self.lr_entry.get())
        self.mlp = MultiLayerPerceptron(self.input_size,
                                        self.hidden_layer_sizes,
                                        self.output_size,
                                        self.learning_rate,
                                        self.loss_function,
                                        MultiLayerPerceptronConfiguration(epochs))
        training_data = self.load_data(r"C:\Users\Воронов Игорь\PycharmProjects\lab2(AI)\dataset.csv")
        self.mlp.train(training_data)
        print(f"Начало обучения с {epochs} эпохами и скоростью обучения {learning_rate}.")

    def load_data(self, file_path):
        matrix_csv_loader = MatrixCsvLoader(file_path)
        return matrix_csv_loader.load_data()

    def predict(self):
        predict = self.mlp.predict(sum(self.pixels, []))
        print(f' Predicted: {ClassLabelMapping.REVERSE_MAPPING[predict]}')


if __name__ == "__main__":
    app = PixelArtApp()
