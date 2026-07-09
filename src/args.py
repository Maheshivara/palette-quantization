import argparse
from dataclasses import dataclass
from pathlib import Path

from color.distance import ReductionStrategy


@dataclass(frozen=True)
class Args:
    input_path: Path
    output_path: Path
    strategies: tuple[ReductionStrategy, ...]
    create_full_lut: bool
    lut_output_dir: Path | None
    lut_path: Path | None
    palette_path: Path | None

    @classmethod
    def from_args(cls) -> Args:
        parser = argparse.ArgumentParser(
            description="Quantize images using a color palette"
        )

        parser.add_argument(
            "input_path",
            type=Path,
            help="Input image file or directory",
        )

        parser.add_argument(
            "output_path",
            type=Path,
            help="Output image file or directory",
        )

        parser.add_argument(
            "-s",
            "--strategy",
            dest="strategies",
            nargs="+",
            choices=[s.name for s in ReductionStrategy],
            help=("Color distance strategies to use. Defaults to all strategies."),
        )

        parser.add_argument(
            "-p",
            "--palette",
            dest="palette_path",
            type=Path,
            help="Palette image used for quantization",
        )

        parser.add_argument(
            "-l",
            "--lut",
            dest="lut_path",
            type=Path,
            help="Existing LUT file to apply",
        )

        parser.add_argument(
            "-c",
            "--create-lut",
            dest="create_full_lut",
            action="store_true",
            help="Generate full LUT(s) from the palette",
        )

        parser.add_argument(
            "--lut-output-dir",
            dest="lut_output_dir",
            type=Path,
            help="Directory where generated LUT files are saved",
        )

        ns = parser.parse_args()

        input_path = ns.input_path.resolve()
        output_path = ns.output_path.resolve()

        if not input_path.exists():
            parser.error(f"Input does not exist: {input_path}")

        if input_path.is_dir() and output_path.suffix:
            parser.error(
                "When input_path is a directory, output_path must be a directory"
            )

        if ns.lut_path:
            if ns.palette_path:
                parser.error("--lut cannot be combined with --palette")

            if ns.create_full_lut:
                parser.error("--lut cannot be combined with --create-lut")

            if ns.lut_output_dir:
                parser.error("--lut cannot be combined with --lut-output-dir")

        if ns.create_full_lut:
            if not ns.palette_path:
                parser.error("--create-lut requires --palette")

            if not ns.lut_output_dir:
                parser.error("--create-lut requires --lut-output-dir")

        if not ns.palette_path and not ns.lut_path:
            parser.error("Either --palette or --lut must be provided")

        if ns.strategies:
            strategies = tuple(ReductionStrategy[name] for name in ns.strategies)
        else:
            strategies = tuple(ReductionStrategy)

        return cls(
            input_path=input_path,
            output_path=output_path,
            strategies=strategies,
            create_full_lut=ns.create_full_lut,
            lut_output_dir=(ns.lut_output_dir.resolve() if ns.lut_output_dir else None),
            lut_path=(ns.lut_path.resolve() if ns.lut_path else None),
            palette_path=(ns.palette_path.resolve() if ns.palette_path else None),
        )
