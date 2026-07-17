import numpy as np
from core.domain.distance import DistanceCalculator


class RedMeanDistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("Red_Mean")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        rmean = (colors[:, 0] + palette_color[0]) / 2

        dr = colors[:, 0] - palette_color[0]
        dg = colors[:, 1] - palette_color[1]
        db = colors[:, 2] - palette_color[2]

        return np.sqrt(
            (2 + rmean / 256) * dr * dr
            + 4 * dg * dg
            + (2 + (255 - rmean) / 256) * db * db
        )
