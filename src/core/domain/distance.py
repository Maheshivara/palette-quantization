from abc import ABC, abstractmethod

import numpy as np


class DistanceCalculator(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        pass
