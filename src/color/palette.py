import numpy as np

from image_io.reader import read_rgb


class Palette:
    def __init__(self, img_path: str):
        img = read_rgb(img_path)

        pixels = img.reshape(-1, 3)
        self.colors = np.unique(pixels, axis=0).astype(np.float32)

    def __len__(self) -> int:
        return len(self.colors)
