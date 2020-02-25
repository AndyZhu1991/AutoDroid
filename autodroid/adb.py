from subprocess import check_output
import os

adb_command = "adb"


def init_adb():
    pass


def cap_screen_pic():
    return check_output(f'{adb_command} exec-out screencap -p')


def click_point(x, y):
    os.system(f'{adb_command} shell input tap {x} {y}')
