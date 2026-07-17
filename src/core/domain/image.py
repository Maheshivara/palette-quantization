from dataclasses import dataclass
from enum import Enum, auto
import numpy as np


class ImageColorSpace(Enum):
    RGB = auto()
    RGBA = auto()


@dataclass(frozen=True)
class Image:
    data: np.ndarray
    color_space: ImageColorSpace

    def get_rgb(self) -> np.ndarray:
        return self.data[..., :3]

    def get_alpha(self) -> np.ndarray | None:
        if self.color_space != ImageColorSpace.RGBA:
            return None

        return self.data[..., 3]
