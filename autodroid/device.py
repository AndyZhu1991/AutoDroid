import autodroid.adb as adb
from autodroid.size import Size


class Device():
    serial: str
    status: str
    screen_size: Size

    def __init__(self, serial: str, status: str) -> None:
        self.serial = serial
        self.status = status

    def init(self):
        self.screen_size = adb.get_screen_size(device=self)
    
    def __str__(self) -> str:
        return "Device" + str(self.__dict__)

    @property
    def id(self) -> str:
        return self.serial

    @property
    def is_avaiable(self) -> bool:
        return self.status == 'device'