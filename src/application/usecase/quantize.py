import os

import numpy as np

from application.usecase.create_lut import CreateLuT
from application.usecase.reader import VALID_IMAGE_EXT, Reader
from core.domain.image import Image, ImageColorSpace
from core.domain.logger import Logger
from core.domain.lut import Lut
from in_out.image.writer import write_image


class Quantize:
    def __init__(
        self,
        image_path: str,
        output_path: str,
        reader: Reader,
        lut_creator: CreateLuT,
        logger: Logger,
        preserve_alpha: bool = True,
        palette_path: str | None = None,
        luts_out_dir: str | None = None,
        luts_input_path: str | None = None,
    ) -> None:
        self._image_path = image_path
        self._preserve_alpha = preserve_alpha
        self._output_path = output_path
        self._reader = reader
        self._lut_creator = lut_creator
        self._logger = logger
        self._palette_path = palette_path
        self._luts_out_dir = luts_out_dir
        self._luts_input_path = luts_input_path

        if self._luts_input_path is None and self._palette_path is None:
            self._logger.error("Can not quantize without a LuT or palette")
            raise ValueError()

    def run(self):
        luts: list[Lut] = list()

        if self._luts_out_dir is not None and self._palette_path is not None:
            luts = self._lut_creator.full(self._palette_path, self._luts_out_dir)

        elif self._luts_input_path is not None:
            luts = self._reader.read_luts(self._luts_input_path)

        if os.path.isfile(self._image_path):
            self._process_image(self._image_path, luts)
            return

        image_paths = os.listdir(self._image_path)
        for fname in image_paths:
            if not fname.endswith(VALID_IMAGE_EXT):
                continue
            p = os.path.join(self._image_path, fname)
            self._process_image(p, luts)

    def _process_image(self, img_path: str, luts: list[Lut]) -> bool:
        img = self._reader.read_image(img_path, self._preserve_alpha)
        file_name = os.path.splitext(os.path.basename(img_path))[0]

        if len(luts) < 1:
            if self._palette_path is None:
                self._logger.error("Need a palette to create LuTs")
                return False

            luts = self._lut_creator.sparse(img_path, self._palette_path)

        for lut in luts:
            self._logger.info(f"Applying {lut.name} to {file_name}")
            quantized_colors = lut.apply(img)
            result = Image(data=quantized_colors, color_space=ImageColorSpace.RGB)
            if self._preserve_alpha:
                alpha = img.get_alpha()
                if alpha is None:
                    alpha = np.full(
                        quantized_colors.shape[:2],
                        255,
                        dtype=quantized_colors.dtype,
                    )

                alpha = alpha[..., np.newaxis]

                result = Image(
                    data=np.concatenate((quantized_colors, alpha), axis=-1),
                    color_space=ImageColorSpace.RGBA,
                )

            if os.path.isdir(self._output_path):
                write_image(
                    result,
                    os.path.join(self._output_path, f"{file_name}.{lut.name}.png"),
                )
            else:
                try:
                    write_image(
                        result,
                        os.path.join(self._output_path, f"{file_name}.{lut.name}.png"),
                    )

                except Exception:
                    self._logger.error("Invalid output path")
                    return False

        return True
