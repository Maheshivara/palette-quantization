import os
from pathlib import Path

import numpy as np
from halo import Halo

from args import Args
from color.distance import ReductionStrategy
from color.palette import Palette
from image_io.reader import read_rgb
from image_io.writer import write_rgb
from lut.lut import Lut


def create_luts(
    palette: Palette,
    args: Args,
) -> dict[ReductionStrategy, Lut]:
    luts = {}

    for strategy in args.strategies:
        with Halo(f"Creating '{strategy.name}' LUT") as spinner:
            try:
                if args.palette_path is None:
                    return luts
                path = (
                    args.lut_output_dir
                    / f"{args.palette_path.stem}.{strategy.name}.png"
                    if args.lut_output_dir
                    else None
                )

                luts[strategy] = Lut.full(
                    palette.colors,
                    strategy,
                    str(path) if path else None,
                )

                spinner.succeed()

            except Exception as e:
                spinner.fail(str(e))

    return luts


def load_luts(args: Args) -> dict[ReductionStrategy, Lut]:
    luts = {}

    if args.lut_path:
        path = args.lut_path
        if path.is_file():
            print(path.name)
            strategy_name = path.name.rsplit(".", 3)[1]
            luts[ReductionStrategy[strategy_name]] = Lut.load(str(args.lut_path))

        elif path.is_dir():
            files = os.listdir(path)
            for f in files:
                p = os.path.join(path, f)
                if f.endswith("png"):
                    strategy_name = f.rsplit(".", 3)[1]
                    luts[ReductionStrategy[strategy_name]] = Lut.load(p)

    return luts


def apply_luts(
    img: np.ndarray,
    img_name: str,
    luts: dict[ReductionStrategy, Lut],
    output_path: Path,
):
    for strategy, lut in luts.items():
        with Halo(f"Applying '{strategy.name}' LUT to {img_name}") as spinner:
            try:
                result = lut.apply(img)

                if output_path.is_dir():
                    path = os.path.join(output_path, f"{img_name}.{strategy.name}.png")
                else:
                    path = output_path

                write_rgb(
                    str(path),
                    result,
                )

                spinner.succeed()

            except Exception as e:
                spinner.fail(str(e))


def load_images(args: Args) -> dict[str, np.ndarray]:
    path = args.input_path
    imgs = {}
    if path.is_file():
        imgs[path.name.rsplit(".", 2)[0]] = read_rgb(str(path))

    elif path.is_dir():
        files = os.listdir(path)
        for f in files:
            p = os.path.join(path, f)
            imgs[f.rsplit(".", 2)[0]] = read_rgb(p)

    return imgs


def main():
    args = Args.from_args()

    imgs = load_images(args)

    full_luts: dict[ReductionStrategy, Lut] = dict()
    sparse_luts: dict[str, dict[ReductionStrategy, Lut]] = dict()

    if args.lut_path:
        full_luts = load_luts(args)

    elif args.palette_path:
        palette = Palette(str(args.palette_path))

        if args.create_full_lut:
            full_luts = create_luts(
                palette,
                args,
            )

        else:
            for name, img in imgs.items():
                lut_dict: dict[ReductionStrategy, Lut] = {}
                for strategy in args.strategies:
                    with Halo(
                        f"Creating '{strategy.name}' sparse LUT for {name}"
                    ) as spinner:
                        try:
                            lut_dict[strategy] = Lut.sparse(
                                img,
                                palette.colors,
                                strategy,
                            )
                            spinner.succeed()

                        except Exception as e:
                            spinner.fail(str(e))

                sparse_luts[name]

    if len(full_luts) > 0:
        for name, img in imgs.items():
            apply_luts(img, name, full_luts, args.output_path)
    else:
        for name, luts in sparse_luts.items():
            img = imgs[name]
            apply_luts(img, name, luts, args.output_path)


if __name__ == "__main__":
    main()
