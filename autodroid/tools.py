import cv2
import numpy as np

import autodroid.adb as adb


def fetch_screen_img(scale_to_dp=False):
    png_raw = adb.cap_screen_pic()
    png_raw = np.asarray(bytearray(png_raw), dtype=np.uint8)
    img = cv2.imdecode(png_raw, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if scale_to_dp:
        img = cv2.resize(img, adb.get_screen_size(in_dp=True), interpolation=cv2.INTER_AREA)

    return img


def match(img, templ_img, match_one=True, threshold=0.6, de_dup=True):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    templ_gray = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, templ_gray, cv2.TM_CCOEFF_NORMED)

    if match_one:
        max = np.max(res)
        loc = np.where(res == max)
        x = loc[1][0]
        y = loc[0][0]
        return (x, y, x + templ_gray.shape[1], y + templ_gray.shape[0])

    loc = np.where(res > threshold)
    loc = sorted(zip(loc[0], loc[1]), key=lambda pos: -res[pos[0]][pos[1]])

    matches = list()
    for y, x in loc:
        matches.append((x, y, x + templ_gray.shape[1], y + templ_gray.shape[0]))

    if de_dup:
        no_dup = list()
        for item in matches:
            if len(no_dup) == 0:
                no_dup.append(item)
            else:
                distance = item[0] - no_dup[-1][0]
                if distance < -5 or distance > 5:
                    no_dup.append(item)
    else:
        no_dup = matches

    return no_dup


def scale_image(origin_image, factor):
    """
    To shrink an image, it will generally look best with cv::INTER_AREA interpolation, 
    whereas to enlarge an image, it will generally look best with cv::INTER_CUBIC (slow) or cv::INTER_LINEAR (faster but still looks OK).
    """
    if factor == 1:
        return origin_image

    if factor > 1:
        inter = cv2.INTER_CUBIC
    else:
        inter = cv2.INTER_AREA
    return cv2.resize(origin_image, (0, 0), fx=factor, fy=factor, interpolation=inter)
