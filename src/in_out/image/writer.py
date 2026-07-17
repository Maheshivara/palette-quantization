import cv2

from core.domain.image import Image, ImageColorSpace


def write_image(img: Image, path: str) -> bool:
    data = None
    match img.color_space:
        case ImageColorSpace.RGB:
            data = cv2.cvtColor(img.data, cv2.COLOR_RGB2BGR)
        case ImageColorSpace.RGBA:
            data = cv2.cvtColor(img.data, cv2.COLOR_RGBA2BGRA)

    if data is None:
        raise ValueError("Invalid image color space")

    return cv2.imwrite(path, data)
