import math
from typing import Optional

from autodroid.point import Point
from autodroid.size import Size

class Rect:

    def __init__(self, left, top, right, bottom) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def __str__(self) -> str:
        return "Rect" + str(self.__dict__)

    def __hash__(self) -> int:
        return hash((self.left, self.top, self.right, self.bottom))

    def __eq__(self, other: 'Rect') -> bool:
        return other and self.left == other.left and self.top == other.top and\
            self.right == other.right and self.bottom == other.bottom

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    @property
    def size(self):
        return Size(self.width(), self.height())

    @property
    def area(self):
        return self.width() * self.height()

    def center_x(self):
        return (self.left + self.right) / 2

    def center_y(self):
        return (self.top + self.bottom) / 2

    def center(self) -> Point:
        return Point(self.center_x(), self.center_y())

    def move(self, delta_x, delta_y):
        self.left += delta_x
        self.top += delta_y
        self.right += delta_x
        self.bottom += delta_y

    def contains(self, x, y) -> bool:
        return x >= self.left and x < self.right and y >= self.top and y < self.bottom

    def contains_rect(self, other: 'Rect') -> bool:
        return self.left <= other.left and self.top <= other.top \
           and self.right >= other.right and self.bottom >= other.bottom

    def is_intersect(self, other: 'Rect') -> bool:
        h_interset = not (self.right < other.left or other.right < self.left)
        v_interset = not (self.bottom < other.top or other.bottom < self.top)
        return h_interset and v_interset

    def intersect_rect(self, other: 'Rect') -> Optional['Rect']:
        if not self.is_intersect(other):
            return None
        else:
            return Rect(max(self.left, other.left), max(self.top, other.top),\
                        min(self.right, other.right), min(self.bottom, other.bottom))

    def union(self, other: 'Rect') -> 'Rect':
        return Rect(min(self.left, other.left), min(self.top, other.top), \
                    max(self.right, other.right), max(self.bottom, other.bottom))

    def copy(self) -> 'Rect':
        return Rect(self.left, self.top, self.right, self.bottom)

    def left_top(self) -> Point:
        return Point(self.left, self.top)

    def scale(self, factor):
        self.left *= factor
        self.right *= factor
        self.top *= factor
        self.bottom *= factor

    def integerlize(self):
        self.left = round(self.left)
        self.top = round(self.top)
        self.right = round(self.right)
        self.bottom = round(self.bottom)

    def limit_in(self, other: 'Rect'):
        """
        Limit self in other Rect. The other Rect MUST larger than self, both width and height
        """
        assert self.width() <= other.width() and self.height() <= other.height()
        if self.left < other.left:
            self.move(other.left - self.left, 0)
        elif self.right > other.right:
            self.move(other.right - self.right, 0)
        if self.top < other.top:
            self.move(0, other.top - self.top)
        elif self.bottom > other.bottom:
            self.move(0, other.bottom - self.bottom)

    @staticmethod
    def from_center_size(center: Point, size: Size) -> 'Rect':
        return Rect(center.x - size.width / 2, center.y - size.height / 2, \
                    center.x + size.width / 2, center.y + size.height / 2)

    @staticmethod
    def from_start_size(start: Point, size: Size) -> 'Rect':
        return Rect(start.x, start.y, start.x + size.width, start.y + size.height)