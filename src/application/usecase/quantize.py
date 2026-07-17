import os

import numpy as np
from application.usecase.create_lut import CreateLuT
from core.domain.logger import Logger
from core.domain.lut import Lut
from application.usecase.reader import Reader
from core.domain.image import Image, ImageColorSpace
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

        elif self._palette_path is not None:
            luts = self._lut_creator.sparse(self._image_path, self._palette_path)

        if len(luts) < 1:
            self._logger.error("Couldn't create a LuT to quantize")
            return

        img = self._reader.read_image(self._image_path, self._preserve_alpha)
        file_name = os.path.splitext(os.path.basename(self._image_path))[0]
        for lut in luts:
            self._logger.info(f"Applying {lut.name} to input")
            quantized_colors = lut.apply(img)

            if self._preserve_alpha:
                alpha = img.get_alpha()
                if alpha is None:
                    alpha = np.full(
                        quantized_colors.shape[:2],
                        255,
                        dtype=quantized_colors.dtype,
                    )

                alpha = alpha[..., np.newaxis]

                final = Image(
                    data=np.concatenate((quantized_colors, alpha), axis=-1),
                    color_space=ImageColorSpace.RGBA,
                )

                if os.path.isdir(self._output_path):
                    write_image(
                        final,
                        os.path.join(self._output_path, f"{file_name}.{lut.name}.png"),
                    )
