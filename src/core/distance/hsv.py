import numpy as np
import cv2
from core.domain.distance import DistanceCalculator


class HSVDistanceCalculator(DistanceCalculator):
    def __init__(self) -> None:
        super().__init__("HSV")

    def calculate(self, colors: np.ndarray, palette_color: np.ndarray) -> np.ndarray:
        hsv_colors = cv2.cvtColor(
            colors.astype(np.uint8).reshape(-1, 1, 3),
            cv2.COLOR_RGB2HSV,
        )[:, 0].astype(np.float32)

        hsv_palette = self._hsv(palette_color)

        dh = np.abs(hsv_colors[:, 0] - hsv_palette[0])
        dh = np.minimum(dh, 180 - dh)

        return np.sqrt(
            dh * dh
            + (hsv_colors[:, 1] - hsv_palette[1]) ** 2
            + (hsv_colors[:, 2] - hsv_palette[2]) ** 2
        )

    def _hsv(self, color):

        rgb = color.astype(np.uint8).reshape(1, 1, 3)

        return cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0, 0].astype(np.float32)
