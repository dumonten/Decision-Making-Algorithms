import copy
import math
import random
import numpy as np


class PotentialClassifier:
    def __init__(self, num_vectors, num_attributes):
        self.num_vectors = num_vectors
        self.num_attributes = num_attributes

        self.function = np.array([], dtype=np.int64)
        self.local_weights = np.array([], dtype=np.int64)
        self.base_weight = np.array([1, 4, 4, 16])
        self.training_set = np.array([], dtype=np.int64)
        self.labels = np.array([], dtype=np.int64)

        self.ro = 0
        self.is_trained = False
        self.iteration_limit = 10_000

        self.training_set, \
            self.labels, self.local_weights = self.generate_training_set(self.num_vectors,
                                                                         self.num_attributes,
                                                                         self.base_weight)

    @staticmethod
    def generate_training_set(num_vectors, num_attributes, base_weight):
        flatten_array = np.random.random_integers(-10, 10, num_vectors * num_attributes)
        flatten_array = flatten_array.astype(np.int64)

        labels = [0 if x < num_vectors // 2 else 1 for x in range(num_vectors)]

        training_set = flatten_array.reshape(num_vectors, num_attributes)
        local_weights = np.zeros((num_vectors, 4), dtype=np.int64)
        for vector_id, vector in enumerate(training_set):
            local_weights[vector_id] = PotentialClassifier.calc_local_weight(vector, base_weight)
        return training_set, labels, local_weights

    def training_set_to_string(self):
        vector_strings = []
        for vector in self.training_set:
            vector_strings.append(f"[{vector[0]}, {vector[1]}]")
        cls_0 = "Класс 0:\n" + "\n".join(vector_strings[:len(vector_strings)//2])
        cls_1 = "Класс 1:\n" + "\n".join(vector_strings[len(vector_strings)//2:])
        return cls_0 + "\n\n" + cls_1

    def function_to_string(self):
        signs = ["+" if coefficient >= 0 else "-" for coefficient in self.function]
        return f"d(x) = {signs[0]} {abs(self.function[0])} {signs[1]} {abs(self.function[1])}x1 " \
                          f"{signs[2]}{abs(self.function[2])}x2 {signs[3]}{abs(self.function[3])}x1x2 "

    def get_decision_function(self):
        self.function = np.array(self.local_weights[0], dtype=np.int64)
        iteration = 0
        while not self.is_trained and iteration <= self.iteration_limit:
            self.is_trained = True
            self.ro = 0
            for vector_id, vector in enumerate(self.training_set[:-1]):
                self.function += self.ro * self.local_weights[vector_id]
                predicted_cls = self.classify(self.training_set[vector_id + 1], self.function)
                self.correction(predicted_cls, self.labels[vector_id + 1])
            predicted_cls = self.classify(self.training_set[0], self.function)
            self.correction(predicted_cls, self.labels[0])
            self.function += self.ro * self.local_weights[0]
            iteration += 1
        return iteration > self.iteration_limit

    def correction(self, predicted_cls, real_cls):
        if predicted_cls > real_cls:
            self.ro = 1
            self.is_trained = False
        elif predicted_cls < real_cls:
            self.ro = -1
            self.is_trained = False
        else:
            self.ro = 0

    @staticmethod
    def calc_local_weight(vector, base):
        return np.array([base[0], base[1] * vector[0], base[2] * vector[1], base[3] * vector[0] * vector[1]],
                        dtype=np.int64)

    @staticmethod
    def calc_function(vector, function):
        return function[0] + function[1] * vector[0] + function[2] * vector[1] \
            + function[3] * vector[0] * vector[1]

    @staticmethod
    def classify(vector, function):
        return 0 if PotentialClassifier.calc_function(vector, function) > 0 else 1

