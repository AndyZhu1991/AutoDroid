from autodroid.image import AndroidImage
import cv2
import numpy as np
from autodroid.adb import cap_screen_pic, get_dpi
from autodroid.rect import Rect


def fetch_screen_img():
    png_raw = cap_screen_pic()
    png_raw = np.asarray(bytearray(png_raw), dtype=np.uint8)
    img = cv2.imdecode(png_raw, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    return AndroidImage(img, get_dpi())


def match(img, templ_img, match_one=True, threshold=0.5, de_dup=True, ignore_dpi=False):
    if img is np.ndarray:
        img = AndroidImage(img)
    if ignore_dpi or img.dpi == templ_img.dpi or img.dpi == None or templ_img.dpi == None:
        coord_scale = 1
        img_array = img.image
        templ_array = templ_img.image
    elif img.dpi < templ_img.dpi:
        coord_scale = 1
        img_array = img.image
        templ_array = scale_image(templ_img.image, img.dpi / templ_img.dpi)
    else:
        coord_scale = img.dpi / templ_img.dpi
        img_array = scale_image(img.image, 1 / coord_scale)
        templ_array = templ_img.image

    def coord_restore(rect):
        return Rect(rect[0] * coord_scale, rect[1] * coord_scale, rect[2] * coord_scale, rect[3] * coord_scale)

    res = cv2.matchTemplate(img_array, templ_array, cv2.TM_CCOEFF_NORMED)

    if match_one:
        max = np.max(res)
        loc = np.where(res == max)
        x = loc[1][0]
        y = loc[0][0]
        if res[y][x] < threshold:
            return None
        result = (x, y, x + templ_array.shape[1], y + templ_array.shape[0])
        return coord_restore(result)

    loc = np.where(res > threshold)
    loc = sorted(zip(loc[0], loc[1]), key=lambda pos: -res[pos[0]][pos[1]])

    matches = list()
    for y, x in loc:
        matches.append((x, y, x + templ_array.shape[1], y + templ_array.shape[0]))

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

    return list(map(lambda item: coord_restore(item), no_dup))


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


def get_image_region(origin_image, rect: Rect):
    if origin_image is AndroidImage:
        image = origin_image.image
        return AndroidImage(image[rect.top:rect.bottom, rect.left:rect.right], origin_image.dpi)
    else:
        return origin_image[rect.top:rect.bottom, rect.left:rect.right]
