import cv2
from core.domain.image import Image, ImageColorSpace


def read_image(path: str, is_rgba: bool = True) -> Image:
    flag = cv2.IMREAD_UNCHANGED if is_rgba else cv2.IMREAD_COLOR

    data = cv2.imread(path, flag)
    if data is None:
        raise FileNotFoundError("Image file not found")

    if is_rgba:
        return Image(
            data=cv2.cvtColor(data, cv2.COLOR_BGRA2RGBA),
            color_space=ImageColorSpace.RGBA,
        )

    return Image(
        data=cv2.cvtColor(data, cv2.COLOR_BGR2RGB), color_space=ImageColorSpace.RGB
    )
