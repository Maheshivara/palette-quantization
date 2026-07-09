import cv2
import numpy as np


def write_rgb(path: str, img: np.ndarray) -> None:
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
