class Point():

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


    def __str__(self) -> str:
        return "Point" + str(self.__dict__)