import os

import numpy as np

from in_out.image.reader import read_image
from in_out.image.writer import write_image
from core.domain.distance import DistanceCalculator
from core.domain.image import Image, ImageColorSpace
from core.domain.palette import Palette


class Lut:
    def __init__(self, lut: np.ndarray | dict, name: str):
        self.lut = lut
        self.name = name

    @classmethod
    def generate_full(
        cls,
        palette: Palette,
        distance_calculator: DistanceCalculator,
        out_dir: str | None = None,
        size: int = 64,
    ) -> "Lut":
        palette_colors = palette.colors
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
                distance_calculator.calculate(colors, palette_color)
                for palette_color in palette_colors
            ],
            axis=1,
        )

        closest = np.argmin(distances, axis=1)

        lut = palette_colors[closest].reshape(size, size, size, 3).astype(np.uint8)

        if out_dir is not None:
            cls._save_cube(
                os.path.join(out_dir, f"{palette.name}.{distance_calculator.name}.png"),
                lut,
            )

        return cls(lut, distance_calculator.name)

    @classmethod
    def load(cls, path: str) -> "Lut":
        image = read_image(path, False)

        color = image.get_rgb()
        size = color.shape[0]

        if color.shape != (size, size * size, 3):
            raise ValueError(f"Invalid LUT shape: {image.data.shape}")

        cube = cls._image_to_cube(image)
        lut_name = path.rsplit(".", 3)[1]
        return cls(cube, lut_name)

    def apply(self, img: Image) -> np.ndarray:
        data = img.get_rgb()
        if isinstance(self.lut, dict):
            h, w, _ = data.shape
            pixels = data.reshape(-1, 3)
            reduced = np.array(
                [self.lut[tuple(pixel)] for pixel in pixels],
                dtype=np.uint8,
            )
            return reduced.reshape(h, w, 3)

        size = self.lut.shape[0]

        coords = (data.astype(np.float32) * (size - 1) / 255).astype(np.int32)

        r = coords[..., 0]
        g = coords[..., 1]
        b = coords[..., 2]

        return self.lut[r, g, b]

    @classmethod
    def generate_sparse(
        cls,
        img: Image,
        palette: Palette,
        distance_calculator: DistanceCalculator,
    ) -> Lut:
        palette_colors = palette.colors
        data = img.get_rgb()
        colors = np.unique(
            data.reshape(-1, 3),
            axis=0,
        ).astype(np.float32)

        distances = np.stack(
            [
                distance_calculator.calculate(
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

        return cls(lut, distance_calculator.name)

    @staticmethod
    def _cube_to_image(cube: np.ndarray) -> Image:
        size = cube.shape[0]
        data = cube.transpose(1, 0, 2, 3).reshape(size, size * size, 3)

        return Image(data=data, color_space=ImageColorSpace.RGB)

    @staticmethod
    def _image_to_cube(image: Image) -> np.ndarray:
        data = image.get_rgb()
        size = data.shape[0]
        return data.reshape(size, size, size, 3).transpose(1, 0, 2, 3)

    @staticmethod
    def _save_cube(path: str, cube: np.ndarray) -> None:
        image = Lut._cube_to_image(cube)
        write_image(image, path)
