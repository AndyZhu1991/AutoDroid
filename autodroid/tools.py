from typing import Union, List
import cv2
import numpy as np
from autodroid.adb import cap_screen_pic
from autodroid.device import Device
from autodroid.rect import Rect
from numpy import ndarray as Image
from autodroid.size import Size


class MatchedRect(Rect):
    def __init__(self, left, top, right, bottom, confidence) -> None:
        super().__init__(left, top, right, bottom)
        self.confidence = confidence


def fetch_screen_img(device: Device = None, use_png=True, timeout=None) -> Image:
    raw = cap_screen_pic(device, use_png=use_png, timeout=timeout)
    img = None
    if use_png:
        png_raw = np.asarray(bytearray(raw), dtype=np.uint8)
        img = cv2.imdecode(png_raw, cv2.IMREAD_COLOR)
    else:
        width = int.from_bytes(raw[0: 4], byteorder='little')
        height = int.from_bytes(raw[4: 8], byteorder='little')
        image = np.frombuffer(raw[-width*height*4:], dtype='uint8')
        image = np.reshape(image, (height, width, 4))
        img = image[:,:,[2, 1, 0]]
 
    return img


def match(img: Image, templ_img: Image, search_rect: Rect = None, match_one=True,\
          threshold=0.666, de_dup=True, img_dpi=None, templ_dpi=None, mask = None\
          )-> Union[MatchedRect, List[MatchedRect]]:

    if search_rect != None:
        img = get_image_region(img, search_rect)

    if img_dpi == None or templ_dpi == None:
        coord_scale = 1
    elif img_dpi < templ_dpi:
        coord_scale = 1
        templ_img = scale_image(templ_img, img_dpi / templ_dpi)
    else:
        coord_scale = img_dpi / templ_dpi
        img = scale_image(img, 1 / coord_scale)

    def coord_restore(rect: List[int], confidence) -> MatchedRect:
        result = MatchedRect(rect[0] * coord_scale, rect[1] * coord_scale,\
                             rect[2] * coord_scale, rect[3] * coord_scale, confidence)
        if search_rect != None:
            result.move(search_rect.left, search_rect.top)
        return result

    res = cv2.matchTemplate(img, templ_img, cv2.TM_CCOEFF_NORMED, mask=mask)

    if match_one:
        max = np.max(res)
        loc = np.where(res == max)
        x = loc[1][0]
        y = loc[0][0]
        if res[y][x] < threshold:
            return None
        result = (x, y, x + templ_img.shape[1], y + templ_img.shape[0])
        return coord_restore(result, res[y][x])

    loc = np.where(res > threshold)
    loc = sorted(zip(loc[0], loc[1]), key=lambda pos: -res[pos[0]][pos[1]])

    matches = list()
    for y, x in loc:
        matches.append(([x, y, x + templ_img.shape[1], y + templ_img.shape[0]], res[y][x]))

    # if de_dup:
    #     no_dup = list()
    #     for item in matches:
    #         if len(no_dup) == 0:
    #             no_dup.append(item)
    #         else:
    #             distance = item[0] - no_dup[-1][0]
    #             if distance < -5 or distance > 5:
    #                 no_dup.append(item)
    # else:
    #     no_dup = matches

    matches = list(map(lambda item: coord_restore(item[0], item[1]), matches))
    de_duped = list()
    for item in matches:
        # has
        if next((x for x in de_duped if item.is_intersect(x)), None) == None:
            de_duped.append(item)
    return de_duped


def scale_image(origin_image: Image, target_size: Size) -> Image:
    """
    To shrink an image, it will generally look best with cv::INTER_AREA interpolation, 
    whereas to enlarge an image, it will generally look best with cv::INTER_CUBIC (slow) or cv::INTER_LINEAR (faster but still looks OK).
    """
    origin_size = get_image_size(origin_image)

    if origin_size == target_size:
        return origin_image

    factor_x = target_size.width / origin_size.width
    factor_y = target_size.height / origin_size.height

    if factor_x > 1 and factor_y > 1:
        inter = cv2.INTER_CUBIC
    else:
        inter = cv2.INTER_AREA

    return cv2.resize(origin_image, (0, 0), fx=factor_x, fy=factor_y, interpolation=inter)


def get_image_region(origin_image: Image, rect: Rect) -> Image:
    return origin_image[rect.top:rect.bottom, rect.left:rect.right]


def read_image(image_path: str) -> Image:
    image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def get_image_size(img: Image) -> Size:
    shape = img.shape
    return Size(shape[1], shape[0])
