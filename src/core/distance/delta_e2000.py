import numpy as np
from core.domain.distance import DistanceCalculator

from skimage.color import (
    rgb2lab,
    deltaE_ciede2000,
)


class DeltaE2000DistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("Delta_E2000")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        lab1 = rgb2lab(colors.reshape(-1, 1, 3) / 255.0)
        lab2 = self._lab(palette_color).reshape(1, 1, 3)

        lab2 = np.repeat(
            lab2,
            len(colors),
            axis=0,
        )

        return deltaE_ciede2000(
            lab1,
            lab2,
        )[:, 0]

    def _lab(self, color: np.ndarray) -> np.ndarray:

        rgb = color.astype(np.float32).reshape(1, 1, 3) / 255.0

        return rgb2lab(rgb)[0, 0]
