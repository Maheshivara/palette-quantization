import os

from core.domain.image import Image
from core.domain.logger import Logger
from core.domain.lut import Lut
from core.domain.palette import Palette
from in_out.image.reader import read_image

VALID_IMAGE_EXT = ("png", "jpg", "webp")


class Reader:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def read_palette(self, palette_path: str) -> Palette:
        if not (
            os.path.isfile(palette_path) and palette_path.endswith(VALID_IMAGE_EXT)
        ):
            self._logger.error("Invalid palette file path")
            raise ValueError()
        try:
            palette = Palette(palette_path)
            return palette

        except Exception:
            self._logger.error("Couldn't read palette file")
            raise ValueError()

    def read_image(self, image_path: str, preserve_alpha: bool = True) -> Image:
        if not (os.path.isfile(image_path) and image_path.endswith(VALID_IMAGE_EXT)):
            self._logger.error("Invalid image file path")
            raise ValueError()

        try:
            img = read_image(image_path, preserve_alpha)
            return img

        except Exception:
            self._logger.error("Couldn't read image file")
            raise ValueError()

    def read_luts(self, luts_path: str) -> list[Lut]:
        luts: list[Lut] = list()

        if os.path.isdir(luts_path):
            for file in os.listdir(luts_path):
                lut_path = os.path.abspath(os.path.join(luts_path, file))
                if not (
                    os.path.isfile(lut_path) and lut_path.endswith(VALID_IMAGE_EXT)
                ):
                    self._logger.debug(f"Skipping {file} as is not a LuT file")
                    continue
                try:
                    lut = Lut.load(lut_path)
                    luts.append(lut)

                except Exception:
                    self._logger.warning(f"Couldn't read LuT file: {file}")

            return luts

        if not (os.path.isfile(luts_path) and luts_path.endswith(VALID_IMAGE_EXT)):
            self._logger.error("Invalid lut file path")
            raise ValueError()

        try:
            lut = Lut.load(luts_path)
            return [lut]

        except Exception:
            self._logger.error(f"Couldn't read LuT file: {luts_path}")
            raise ValueError()
