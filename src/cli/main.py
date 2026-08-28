from cli.args import Args
from application.usecase.quantize import Quantize
from application.usecase.reader import Reader
from application.usecase.create_lut import CreateLuT
from cli.logger import CLILogger


class CLI:
    def run(self):
        args = Args.from_args()
        logger = CLILogger()
        reader = Reader(logger)
        lut_creator = CreateLuT(reader, set(args.strategies), logger)
        quantize = Quantize(
            str(args.input_path),
            str(args.output_path),
            reader,
            lut_creator,
            logger,
            True,
            str(args.palette_path) if args.palette_path else None,
            str(args.lut_output_dir) if args.lut_output_dir else None,
            str(args.lut_path) if args.lut_path else None,
        )

        quantize.run()
