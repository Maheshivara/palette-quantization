import numpy as np

from color.distance import ColorDistanceCalculator, ReductionStrategy
from image_io.reader import read_rgb
from image_io.writer import write_rgb


class Lut:
    def __init__(self, lut: np.ndarray | dict):
        self.lut = lut

    @classmethod
    def full(
        cls,
        palette_colors: np.ndarray,
        strategy: ReductionStrategy,
        path: str | None = None,
        size: int = 64,
    ) -> "Lut":
        calculator = ColorDistanceCalculator(strategy)

        values = np.linspace(0, 255, size, dtype=np.float32)

        r, g, b = np.meshgrid(values, values, values, indexing="ij")

        colors = np.column_stack(
            (
                r.ravel(),
                g.ravel(),
                b.ravel(),
            )
        )

        distances = np.stack(
            [
                calculator.calculate(colors, palette_color)
                for palette_color in palette_colors
            ],
            axis=1,
        )

        closest = np.argmin(distances, axis=1)

        lut = palette_colors[closest].reshape(size, size, size, 3).astype(np.uint8)

        if path is not None:
            cls.save_cube(path, lut)

        return cls(lut)

    @classmethod
    def load(cls, path: str) -> "Lut":
        image = read_rgb(path)

        size = image.shape[0]

        if image.shape != (size, size * size, 3):
            raise ValueError(f"Invalid LUT shape: {image.shape}")

        cube = cls._image_to_cube(image)

        return cls(cube)

    def apply(self, img: np.ndarray) -> np.ndarray:
        if isinstance(self.lut, dict):
            h, w, _ = img.shape
            pixels = img.reshape(-1, 3)
            reduced = np.array(
                [self.lut[tuple(pixel)] for pixel in pixels],
                dtype=np.uint8,
            )
            return reduced.reshape(h, w, 3)

        size = self.lut.shape[0]

        coords = (img.astype(np.float32) * (size - 1) / 255).astype(np.int32)

        r = coords[..., 0]
        g = coords[..., 1]
        b = coords[..., 2]

        return self.lut[r, g, b]

    @classmethod
    def sparse(
        cls,
        img: np.ndarray,
        palette_colors: np.ndarray,
        strategy: ReductionStrategy,
    ) -> Lut:
        calculator = ColorDistanceCalculator(strategy)

        colors = np.unique(
            img.reshape(-1, 3),
            axis=0,
        ).astype(np.float32)

        distances = np.stack(
            [
                calculator.calculate(
                    colors,
                    palette_color,
                )
                for palette_color in palette_colors
            ],
            axis=1,
        )

        closest = np.argmin(
            distances,
            axis=1,
        )

        mapped = palette_colors[closest]

        lut = {
            tuple(color.astype(np.uint8)): mapped_color.astype(np.uint8)
            for color, mapped_color in zip(colors, mapped)
        }

        return cls(lut)

    @staticmethod
    def _cube_to_image(cube: np.ndarray) -> np.ndarray:
        size = cube.shape[0]
        return cube.transpose(1, 0, 2, 3).reshape(size, size * size, 3)

    @staticmethod
    def _image_to_cube(image: np.ndarray) -> np.ndarray:
        size = image.shape[0]
        return image.reshape(size, size, size, 3).transpose(1, 0, 2, 3)

    @staticmethod
    def save_cube(path: str, cube: np.ndarray) -> None:
        image = Lut._cube_to_image(cube)
        write_rgb(path, image)
