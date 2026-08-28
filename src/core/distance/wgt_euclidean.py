import numpy as np
from core.domain.distance import DistanceCalculator


class WGTEuclideanDistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("Wgt_Euclidean")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        d = colors - palette_color
        return np.sqrt(
            0.299 * d[:, 0] ** 2 + 0.587 * d[:, 1] ** 2 + 0.114 * d[:, 2] ** 2
        )
