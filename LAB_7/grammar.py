import matplotlib.pyplot as plt
import numpy.random as rnd
from abc import ABC, abstractmethod


L_RULE = 0
D_RULE = 1


class Point(ABC):
    @abstractmethod
    def __init__(self, x, y, rand_c):
        self.parent = None
        self.left = None
        self.right = None
        self.line_length = 10
        self.x = x
        self.y = y
        self.noise()

    def noise(self):
        self.x += rnd.rand() * 2 - 1
        self.y += rnd.rand() * 2 - 1


class EndPoint(Point):
    @abstractmethod
    def __init__(self, parent, x, y, rand_c):
        super().__init__(x, y, rand_c)
        self.parent = parent
        if rand_c:
            self.random()

    @abstractmethod
    def plot(self, ax):
        pass

    def random(self):
        self.x += (rnd.rand() - 1) * 40
        self.y += (rnd.rand() - 1) * 40


class HorizontalLine(EndPoint):
    def __init__(self, parent, x, y, rand_c):
        super().__init__(parent, x, y, rand_c)

    def plot(self, ax):
        ax.hlines(y=self.y, xmin=self.x, xmax=self.x + self.line_length, colors='black')


class VerticalLine(EndPoint):
    def __init__(self, parent, x, y, rand_c):
        super().__init__(parent, x, y, rand_c)

    def plot(self, ax):
        ax.vlines(x=self.x, ymin=self.y, ymax=self.y + self.line_length, colors='black')


class TwoVerticalLines(Point):
    def __init__(self, parent, x, y, rand_c):
        super().__init__(x, y, rand_c)
        self.parent = parent
        self.left = VerticalLine(self, x, y, rand_c)
        self.right = VerticalLine(self, x + self.line_length, y, rand_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = L_RULE


class TwoVerticalOneDownHorizontalLines(Point):
    def __init__(self, parent, x, y, rand_c):
        super().__init__(x, y, rand_c)
        self.parent = parent
        self.left = TwoVerticalLines(self, x, y, rand_c)
        self.right = HorizontalLine(self, x, y + self.line_length, rand_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = D_RULE


class Square(Point):
    def __init__(self, parent, x, y, random_c):
        super().__init__(x, y, random_c)
        self.parent = parent
        self.left = HorizontalLine(self, x, y, random_c)
        self.right = TwoVerticalOneDownHorizontalLines(self, x, y, random_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = D_RULE


class DoubleSquare(Point):
    def __init__(self, parent, x, y, random_c):
        super().__init__(x, y, random_c)
        self.parent = parent
        self.left = Square(self, x - self.line_length, y, random_c)
        self.right = Square(self, x, y, random_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = L_RULE


class TripleSquare(Point):
    def __init__(self, parent, x, y, random_c):
        super().__init__(x, y, random_c)
        self.parent = parent
        self.left = DoubleSquare(self, x - self.line_length, y, random_c)
        self.right = Square(self, x, y, random_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = L_RULE


class HatForm(Point):
    def __init__(self, parent, x, y, rand_c):
        super().__init__(x, y, rand_c)
        self.parent = parent
        self.left = Square(self, x, y - self.line_length, rand_c)
        self.right = TripleSquare(self, x + 2 * self.line_length, y, rand_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = D_RULE


class SnakeShape(Point):
    def __init__(self, x, y, rand_c):
        super().__init__(x, y, rand_c)
        self.left = TripleSquare(self, x, y, rand_c)
        self.right = HatForm(self, x, y + 2 * self.line_length, rand_c)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = D_RULE


class Grammar:
    def __init__(self, rand_c):
        self.grammar_tree = SnakeShape(0, 0, rand_c)

    def draw(self, ax, current_node=None):
        if current_node is None:
            current_node = self.grammar_tree
        if current_node.left is None:
            current_node.plot(ax)
            return
        self.draw(ax, current_node.left)
        self.draw(ax, current_node.right)

    def check_rules(self, current_node=None):
        if current_node is None:
            current_node = self.grammar_tree
        if current_node.left is None:
            return True
        correct = None
        if current_node.rule == L_RULE:
            correct = current_node.left.x <= current_node.right.x
        else:
            correct = current_node.left.y <= current_node.right.y
        correct &= self.check_rules(current_node.left)
        correct &= self.check_rules(current_node.right)
        return correct

