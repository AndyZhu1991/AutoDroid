import autodroid.adb as adb
from autodroid.size import Size


class Device():
    id: str
    screen_size: Size

    def __init__(self, id: str) -> None:
        self.id = id

    def init(self):
        self.screen_size = adb.get_screen_size(device=self)
    
    def __str__(self) -> str:
        return "Device" + str(self.__dict__)