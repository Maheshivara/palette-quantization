import numpy as np
from core.domain.distance import DistanceCalculator


class SQREuclideanDistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("Sqr_Euclidean")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        d = colors - palette_color
        return np.sum(d * d, axis=1)
