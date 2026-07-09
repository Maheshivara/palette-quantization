from enum import Enum, auto

import cv2
import numpy as np
from skimage.color import (
    deltaE_ciede94,
    deltaE_ciede2000,
    rgb2lab,
)


class ReductionStrategy(Enum):
    SQR_EUCLIDEAN = auto()
    WGT_EUCLIDEAN = auto()
    MANHATTAN = auto()
    RED_MEAN = auto()
    HSV_DISTANCE = auto()
    CIELAB = auto()
    DELTA_E94 = auto()
    DELTA_E2000 = auto()


class ColorDistanceCalculator:
    def __init__(self, strategy: ReductionStrategy):
        self.strategy = strategy

    def _squared_euclidean(self, c1, c2):
        d = c1 - c2
        return float(np.dot(d, d))

    def _weighted_euclidean(self, c1, c2):
        d = c1 - c2

        return float(np.sqrt(0.299 * d[0] ** 2 + 0.587 * d[1] ** 2 + 0.114 * d[2] ** 2))

    def _manhattan(self, c1, c2):
        return float(np.abs(c1 - c2).sum())

    def _red_mean(self, c1, c2):

        rmean = (c1[0] + c2[0]) / 2

        dr = c1[0] - c2[0]
        dg = c1[1] - c2[1]
        db = c1[2] - c2[2]

        return float(
            np.sqrt(
                (2 + rmean / 256) * dr * dr
                + 4 * dg * dg
                + (2 + (255 - rmean) / 256) * db * db
            )
        )

    def _hsv(self, color):

        rgb = color.astype(np.uint8).reshape(1, 1, 3)

        return cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0, 0].astype(np.float32)

    def _lab(self, color):

        rgb = color.astype(np.float32).reshape(1, 1, 3) / 255.0

        return rgb2lab(rgb)[0, 0]

    def _hsv_distance(self, c1, c2):

        h1, s1, v1 = self._hsv(c1)
        h2, s2, v2 = self._hsv(c2)

        dh = abs(h1 - h2)
        dh = min(dh, 180 - dh)

        return float(np.sqrt(dh * dh + (s1 - s2) ** 2 + (v1 - v2) ** 2))

    def _cielab(self, c1, c2):

        return float(np.linalg.norm(self._lab(c1) - self._lab(c2)))

    def _delta_e94(self, c1, c2):

        return float(
            deltaE_ciede94(
                self._lab(c1).reshape(1, 1, 3), self._lab(c2).reshape(1, 1, 3)
            )[0, 0]
        )

    def _delta_e2000(self, c1, c2):

        return float(
            deltaE_ciede2000(
                self._lab(c1).reshape(1, 1, 3), self._lab(c2).reshape(1, 1, 3)
            )[0, 0]
        )

    def calculate(
        self,
        colors: np.ndarray,
        palette_color: np.ndarray,
    ) -> np.ndarray:

        match self.strategy:
            case ReductionStrategy.SQR_EUCLIDEAN:
                d = colors - palette_color
                return np.sum(d * d, axis=1)

            case ReductionStrategy.WGT_EUCLIDEAN:
                d = colors - palette_color
                return np.sqrt(
                    0.299 * d[:, 0] ** 2 + 0.587 * d[:, 1] ** 2 + 0.114 * d[:, 2] ** 2
                )

            case ReductionStrategy.MANHATTAN:
                return np.abs(colors - palette_color).sum(axis=1)

            case ReductionStrategy.RED_MEAN:
                rmean = (colors[:, 0] + palette_color[0]) / 2

                dr = colors[:, 0] - palette_color[0]
                dg = colors[:, 1] - palette_color[1]
                db = colors[:, 2] - palette_color[2]

                return np.sqrt(
                    (2 + rmean / 256) * dr * dr
                    + 4 * dg * dg
                    + (2 + (255 - rmean) / 256) * db * db
                )

            case ReductionStrategy.CIELAB:
                lab1 = rgb2lab(colors.reshape(-1, 1, 3) / 255.0)
                lab2 = self._lab(palette_color)

                return np.linalg.norm(
                    lab1[:, 0, :] - lab2,
                    axis=1,
                )

            case ReductionStrategy.DELTA_E94:
                lab1 = rgb2lab(colors.reshape(-1, 1, 3) / 255.0)
                lab2 = self._lab(palette_color).reshape(1, 1, 3)

                lab2 = np.repeat(
                    lab2,
                    len(colors),
                    axis=0,
                )

                return deltaE_ciede94(
                    lab1,
                    lab2,
                )[:, 0]

            case ReductionStrategy.DELTA_E2000:
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

            case ReductionStrategy.HSV_DISTANCE:
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

            case _:
                raise ValueError(f"Unsupported strategy {self.strategy}")
