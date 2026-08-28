import os

import numpy as np

from in_out.image.reader import read_image


class Palette:
    def __init__(self, img_path: str):
        img = read_image(img_path, False)

        pixels = img.get_rgb().reshape(-1, 3)
        self.colors = np.unique(pixels, axis=0).astype(np.float32)
        self.name = os.path.splitext(os.path.basename(img_path))[0]

    def __len__(self) -> int:
        return len(self.colors)
