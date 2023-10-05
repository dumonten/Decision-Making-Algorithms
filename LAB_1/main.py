import random
import matplotlib.pyplot as plt
import numpy as np


MIN_NUM_OF_KERNELS = 10
MAX_NUM_OF_KERNELS = 10
MIN_NUM_OF_POINTS = 10000
MAX_NUM_OF_POINTS = 10000


class Selection:
    def __init__(self, kernel):
        self.points = list()
        self.kernel = kernel
        self.color = np.random.rand(1, 3)
        self.average = [0.0, 0.0]

    def set_points(self, points):
        self.points = points

    def append_point(self, point):
        self.points.append(point)

    def draw_points(self):
        _x = [point[0] for point in self.points]
        _y = [point[1] for point in self.points]
        plt.scatter(_x, _y, s=5, color=self.color)
        plt.scatter(self.kernel[0], self.kernel[1], s=10, color='black')

    def update_average_value(self):
        self.average = np.array([0.0, 0.0])
        for point in self.points:
            self.average = self.average + point
        self.average = self.average/len(self.points)


def define_array(size):
    _points = list()
    for i in range(0, size):
        point = {"x": random.random(), "y": random.random()}
        _points.append(point)
    _array = np.array([np.array([point['x'], point['y']]) for point in _points])
    return _array


def get_closest_index(_pivot_point, _points):
    _list = [[abs(_pivot_point[0] - x), abs(_pivot_point[1] - y)] for x, y in _points]
    _norms = [np.linalg.norm(x) for x in _list]
    index = _norms.index(min(_norms))
    return index


def separate_points(_selection, _points, _kernels):
    for select in _selection:
        select.points.clear()
    for point in _points:
        closest_kernel_index = get_closest_index(point, _kernels)
        _selection[closest_kernel_index].append_point(point)
    return _selection


def draw(_selection, _iteration):
    plt.figure(_iteration)
    plt.suptitle(f"Iteration {_iteration}")
    for select in _selection:
        select.draw_points()


def updating_kernels(_selection):
    result = False
    for select in _selection:
        select.update_average_value()
        new_kernel = select.points[get_closest_index(select.average, select.points)]
        if not np.array_equal(new_kernel, select.kernel):
            select.kernel = new_kernel
            result = True
    return result


def main():
    size_of_kernels = random.randint(MIN_NUM_OF_KERNELS, MAX_NUM_OF_KERNELS)
    size_of_points = random.randint(MIN_NUM_OF_POINTS, MAX_NUM_OF_POINTS)

    plane = define_array(size_of_kernels + size_of_points)

    kernels = plane[0:size_of_kernels]
    points = plane[:]

    iteration = 0
    selection = list()
    for kernel in kernels:
        selection.append(Selection(kernel))

    selection = separate_points(_selection=selection, _points=points, _kernels=kernels)
    draw(selection, iteration)

    while updating_kernels(selection):
        kernels = [select.kernel for select in selection]
        selection = separate_points(_selection=selection, _points=points, _kernels=kernels)
        iteration += 1
        draw(selection, iteration)
        print(iteration)
    plt.show()


if __name__ == '__main__':
    main()

