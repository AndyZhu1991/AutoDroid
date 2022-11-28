import math


class Point():

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


    def __str__(self) -> str:
        return "Point" + str(self.__dict__)


    def moved(self, delta_x, delta_y) -> "Point":
        return Point(self.x + delta_x, self.y + delta_y)


    def distance(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


    def interpolate(self, other: "Point", fraction: float) -> "Point":
        """
        Returns a point that lies a fraction of the way between this point and the specified point.
        """
        return Point(self.x + (other.x - self.x) * fraction, self.y + (other.y - self.y) * fraction)