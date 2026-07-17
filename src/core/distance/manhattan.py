import numpy as np
from core.domain.distance import DistanceCalculator


class ManhattanDistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("Manhattan")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        return np.abs(colors - palette_color).sum(axis=1)
