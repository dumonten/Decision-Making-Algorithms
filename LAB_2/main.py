import numpy as np
import matplotlib.pyplot as plt
import random

MIN_NUM_OF_POINTS = 10000
MAX_NUM_OF_POINTS = 10000


class Sum:
    def __init__(self):
        self._sum = 0

    def add(self, point_1, point_2):
        self._sum += np.linalg.norm([abs(point_1[0] - point_2[0]),
                                     abs(point_1[1] - point_2[1])])

    def get_sum(self):
        return self._sum


class Selection:
    def __init__(self, kernel):
        self.kernel = kernel
        self._points, self._x, self._y = list(), list(), list()
        self.color = np.random.rand(1, 3)

    def set_points(self, points):
        self._points = points
        self._x = [point[0] for point in self._points]
        self._y = [point[1] for point in self._points]

    def add_point(self, point):
        self._points.append(point)
        self._x.append(point[0])
        self._y.append(point[1])

    def draw_points(self):
        plt.scatter(self._x, self._y, s=5, color=self.color)
        plt.scatter(self.kernel[0], self.kernel[1], s=10, color='black', linestyle='solid')


def draw(selection, iteration):
    plt.figure(iteration)
    plt.suptitle(f"Iteration {iteration}")
    for select in selection:
        select.draw_points()


def get_closest_item_index(pivot_point, selection):
    norms = [np.linalg.norm([abs(pivot_point[0] - select.kernel[0]), abs(pivot_point[1] - select.kernel[1])]) for select in selection]
    return norms.index(min(norms))


def get_further_item(pivot_point, points):
    distances = [np.linalg.norm([abs(pivot_point[0] - x), abs(pivot_point[1] - y)]) for x, y in points]
    max_d = max(distances)
    return distances.index(max_d), max_d


def separate_points(selection, points):
    for select in selection:
        select._points = list()
    for point in points:
        closest_kernel_index = get_closest_item_index(point, selection)
        selection[closest_kernel_index].add_point(point)
    return selection


def generating_kernels(selection, points, sum_ds):
    result, max_ds = False, list()
    for i, select in enumerate(selection):
        max_ds.append([i, *get_further_item(select.kernel, select._points)])
    index_of_a_kernel, further_item_index, dist = max(max_ds, key=lambda x: x[2])

    if dist > (sum_ds.get_sum() / (len(selection) * (len(selection) - 1) * 1.2)):
        new_kernel = selection[index_of_a_kernel]._points[further_item_index]
        for select in selection:
            sum_ds.add(new_kernel, select.kernel)
        selection.append(Selection(new_kernel))
        result = True
    return result


def main():
    n = random.randint(MIN_NUM_OF_POINTS, MAX_NUM_OF_POINTS)
    points = np.array([np.random.rand(2) for _ in range(0, n)])
    selection = [Selection(points[random.randint(0, n - 1)])]
    second_point_index, _ = get_further_item(selection[0].kernel, points)
    selection.append(Selection(points[second_point_index]))
    selection = separate_points(selection=selection, points=points)

    sum_ds, iteration = Sum(), 0
    sum_ds.add(selection[0].kernel, selection[1].kernel)
    draw(selection=selection, iteration=iteration)

    while generating_kernels(selection=selection, points=points, sum_ds=sum_ds):
        selection = separate_points(selection=selection, points=points)
        iteration += 1
        draw(selection=selection, iteration=iteration)
        print(iteration)
    plt.show()


if __name__ == '__main__':
    main()
