import copy
import math
import random
import numpy as np


class PerceptronClass:
    def __init__(self):
        self.objects = []


class PerceptronObject:
    def __init__(self):
        self.attributes = []

    @staticmethod
    def set_data(lst_str, num):
        try:
            attributes = list(map(int, lst_str.split(", ")))
        except Exception:
            return None
        if num != len(attributes):
            return None
        else:
            obj = PerceptronObject()
            obj.attributes = copy.deepcopy(attributes)
            return obj


class Perceptron:
    def __init__(self, classes_num, objects_per_class_num, attributes_num):
        self.constant = 1
        self.max_attribute_value = 10
        self.max_iteration_num = 10_000

        self.classes_num = classes_num
        self.objects_per_class_num = objects_per_class_num
        self.attributes_num = attributes_num

        self.classes = []
        self.weights = []

    def generate_random_classes(self):
        for i in range(self.classes_num):
            pclass = PerceptronClass()
            for j in range(self.objects_per_class_num):
                pobject = PerceptronObject()
                for k in range(self.attributes_num):
                    pobject.attributes.append(random.randint(-self.max_attribute_value, self.max_attribute_value))
                pobject.attributes.append(1)
                pclass.objects.append(pobject)
            self.classes.append(pclass)
        for i in range(self.classes_num):
            self.weights.append(PerceptronObject())
            self.weights[i].attributes = [0] * (self.attributes_num + 1)

    def get_decision_functions(self):
        result, it = True, 0
        while result and it < self.max_iteration_num:
            for pivot, pclass in enumerate(self.classes):
                for pobject in pclass.objects:
                    decisions = [np.dot(weight.attributes, pobject.attributes)
                                 for weight in self.weights]
                    result = False
                    for ind, d in enumerate(decisions):
                        if ind == pivot:
                            continue
                        if decisions[pivot] <= d:
                            result = True
                            self.weights[ind].attributes -= np.dot(self.constant, pobject.attributes)
                    if result:
                        self.weights[pivot].attributes += np.dot(self.constant, pobject.attributes)
            it += 1
        print(it)
        return self.weights

    def get_class(self, pobject):
        result_class = 0
        pobject.attributes.append(1)
        decisions = [np.dot(weight.attributes, pobject.attributes)
                     for weight in self.weights]
        _ = -math.inf
        for i in range(self.classes_num):
            if decisions[i] > _:
                _ = decisions[i]
                result_class = i
        return result_class

    @staticmethod
    def functions_to_string(classes_num, functions):
        strs = [""] * classes_num
        for i, weight in enumerate(functions):
            strs[i] = f'd{i}(x) = '
            for j, attr in enumerate(weight.attributes[:-1]):
                if attr < 0:
                    strs[i] += f'({attr})*x{j} + '
                else:
                    strs[i] += f'{attr}*x{j} + '
            strs[i] += f'{weight.attributes[-1]}'
        return "\n\n".join(strs)

    def classes_to_string(self):
        result = ''
        for iclass, pclass in enumerate(self.classes):
            result += f'Класс [{iclass}]:\n'
            for iobject, pobject in enumerate(pclass.objects):
                result += f'\tОбъект [{iobject}]: ('
                for attr in pobject.attributes[:-2]:
                    result += f'{attr}, '
                result += f'{pobject.attributes[-2]})\n'
        return result
