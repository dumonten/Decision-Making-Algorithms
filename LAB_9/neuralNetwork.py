import numpy as np
import scipy as sc
import pickle
from scipy.ndimage import center_of_mass
import math
import cv2


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes

        self.lr = learning_rate

        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        self.activation_function = sc.special.expit

    def train(self, lst_input, lst_targets):
        inputs = np.array(lst_input, ndmin=2).T
        targets = np.array(lst_targets, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        output_errors = targets - final_outputs

        hidden_errors = np.dot(self.who.T, output_errors)

        self.who += self.lr * np.dot((output_errors *
                                      final_outputs * (1.0 - final_outputs)),
                                      np.transpose(hidden_outputs))

        self.wih += self.lr * np.dot((hidden_errors *
                                      hidden_outputs * (1.0 - hidden_outputs)),
                                      np.transpose(inputs))

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

    @staticmethod
    def _getBestShift(img):
        cy, cx = center_of_mass(img)

        rows, cols = img.shape
        shiftx = np.round(cols / 2.0 - cx).astype(int)
        shifty = np.round(rows / 2.0 - cy).astype(int)

        return shiftx, shifty

    @staticmethod
    def _shift(img, sx, sy):
        rows, cols = img.shape
        M = np.float32([[1, 0, sx], [0, 1, sy]])
        shifted = cv2.warpAffine(img, M, (cols, rows))
        return shifted

    @staticmethod
    def _prep_digit(img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        gray = 255 - img
        # применяем пороговую обработку
        (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # удаляем нулевые строки и столбцы
        while np.sum(gray[0]) == 0:
            gray = gray[1:]
        while np.sum(gray[:, 0]) == 0:
            gray = np.delete(gray, 0, 1)
        while np.sum(gray[-1]) == 0:
            gray = gray[:-1]
        while np.sum(gray[:, -1]) == 0:
            gray = np.delete(gray, -1, 1)
        rows, cols = gray.shape

        # изменяем размер, чтобы помещалось в box 20x20 пикселей
        if rows > cols:
            factor = 20.0 / rows
            rows = 20
            cols = int(round(cols * factor))
            gray = cv2.resize(gray, (cols, rows))
        else:
            factor = 20.0 / cols
            cols = 20
            rows = int(round(rows * factor))
            gray = cv2.resize(gray, (cols, rows))

        # расширяем до размера 28x28
        colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
        rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
        gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')

        # сдвигаем центр масс
        shiftx, shifty = NeuralNetwork._getBestShift(gray)
        shifted = NeuralNetwork._shift(gray, shiftx, shifty)
        gray = shifted

        cv2.imwrite('image/gray.png', gray)
        return gray

    def query_image(self, image_path):
        img_array = self._prep_digit(image_path)
        img_array = img_array.reshape(self.inodes)
        return np.argmax(self.query(img_array))

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_name):
        with open(file_name, 'rb') as file:
            obj = pickle.load(file)
        return obj

    @staticmethod
    def get_load_file_name(input_nodes, hidden_nodes, output_nodes, learning_rate):
        return f"weights-{input_nodes}-{hidden_nodes}-{output_nodes}-{learning_rate}"


def test(nn):
    file = open("mnist_dataset/mnist_test.csv", 'r')
    lst_data = file.readlines()
    file.close()
    scorecard = []

    for record in lst_data[1:]:
        all_values = record.split(',')
        correct_label = int(all_values[0])
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        outputs = nn.query(inputs)
        label = np.argmax(outputs)
        if label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)
    scorecard_array = np.asarray(scorecard)
    print("эффективность = ", scorecard_array.sum() / scorecard_array.size)


def train(nn, epochs=5):
    file = open("mnist_dataset/mnist_train.csv", 'r')
    lst_data = file.readlines()
    file.close()
    scorecard = []

    print("Тренировка...")
    for e in range(epochs):
        print(f"Эпоха №{e}")
        for record in lst_data[1:]:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            targets = np.zeros(nn.onodes) + 0.01
            targets[int(all_values[0])] = 0.99
            nn.train(inputs, targets)





