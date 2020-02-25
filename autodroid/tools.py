from subprocess import check_output

import numpy as np
import cv2

import autodroid.adb as adb


def fetch_screen_img():
    png_raw = adb.cap_screen_pic()
    png_raw = np.asarray(bytearray(png_raw), dtype=np.uint8)
    img = cv2.imdecode(png_raw, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
