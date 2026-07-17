import numpy as np
from core.domain.distance import DistanceCalculator

from skimage.color import (
    rgb2lab,
)


class CIELABDistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("CIELAB")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        lab1 = rgb2lab(colors.reshape(-1, 1, 3) / 255.0)
        lab2 = self._lab(palette_color)

        return np.linalg.norm(
            lab1[:, 0, :] - lab2,
            axis=1,
        )

    def _lab(self, color: np.ndarray) -> np.ndarray:

        rgb = color.astype(np.float32).reshape(1, 1, 3) / 255.0

        return rgb2lab(rgb)[0, 0]
