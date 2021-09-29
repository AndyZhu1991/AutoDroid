class Rect:
    def __init__(self, left, top, right, bottom) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def center_x(self):
        return (self.left + self.right) / 2

    def center_y(self):
        return (self.top + self.bottom) / 2

    def move(self, delta_x, delta_y):
        self.left += delta_x
        self.top += delta_y
        self.right += delta_x
        self.bottom += delta_y

    def contains(self, x, y) -> bool:
        return x >= self.left and x <= self.right and y >= self.top and y <= self.bottom

    def is_intersect(self, other):
        h_interset = not (self.right < other.left or other.right < self.left)
        v_interset = not (self.bottom < other.top or other.bottom < self.top)
        return h_interset and v_interset