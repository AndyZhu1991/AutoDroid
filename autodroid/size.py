class Size():

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height


    def __eq__(self, o) -> bool:
        return self.width == o.width and self.height == o.height


    def __str__(self) -> str:
        return "Device" + str(self.__dict__)