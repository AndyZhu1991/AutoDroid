import cv2


class AndroidImage:
    """
    A class contains a real image and a scale factor(dpi) for Android
    """

    def __init__(self, image, dpi=None) -> None:
        if isinstance(image, str):
            self.image = read_image(image)
        else:
            self.image = image
        self.dpi = dpi


def read_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def read_android_image(image_path):
    return AndroidImage(read_image(image_path))
