import os

from core.distance.factory import DistanceCalculatorFactory, DistanceType
from core.domain.logger import Logger
from core.domain.lut import Lut
from application.usecase.reader import Reader


class CreateLuT:
    def __init__(
        self, reader: Reader, distance_types: set[DistanceType], logger: Logger
    ) -> None:
        self._distance_types = distance_types
        self._logger = logger
        self._reader = reader

    def full(self, palette_path: str, output_dir: str) -> list[Lut]:
        if not os.path.isdir(output_dir):
            self._logger.error("Invalid LuTs output dir path")
            raise ValueError()

        palette = self._reader.read_palette(palette_path)

        luts: list[Lut] = list()

        for type in self._distance_types:
            self._logger.info(f"Creating full LuT for {type.name}")
            calculator = DistanceCalculatorFactory.create(type)
            lut = Lut.generate_full(palette, calculator, output_dir)
            luts.append(lut)

        return luts

    def sparse(self, img_path: str, palette_path: str) -> list[Lut]:
        img = self._reader.read_image(img_path)
        palette = self._reader.read_palette(palette_path)

        luts: list[Lut] = list()

        for type in self._distance_types:
            self._logger.info(f"Creating sparse LuT for {type.name}")
            calculator = DistanceCalculatorFactory.create(type)
            lut = Lut.generate_sparse(img, palette, calculator)
            luts.append(lut)

        return luts
