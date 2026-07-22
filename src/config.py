from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description="Synthetic Dataset Generator")


def parse_args():
    parser.add_argument('--object', type=str, default='bottle',
                        help='Name of the .blend object. Object should be single in the .blend file. The first object from .blend file is used')
    parser.add_argument('--n-images', '-n', type=int, default=1,
                        help='Number of images to generate')
    parser.add_argument('--objects-dir', type=Path, default=Path('input/blend'),
                        help='Directory with .blend objects')
    parser.add_argument('--output-dir', '-od', type=Path, default=Path('output'),
                        help='Directory to output .hdf5 files')
    parser.add_argument('--strict-center', action='store_true',
                        help='Reposition objects at frame center after simulation')
    parser.add_argument('--append-out', '-ao', action='store_true',
                        help='Auto append frame name in out folder')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite existing .hdf5 files in output folder')
    parser.add_argument('--seed', type=int, default=69,
                        help='Seed for random number generator')

    setup_args = parser.add_argument_group('Setup arguments')
    setup_args.add_argument('--conveyor-height', '-ch', type=float, default=0.7,
                            help='Conveyor height in meters from ground')
    setup_args.add_argument('--conveyor-width', '-cw', type=float, default=0.5,
                            help='Conveyor width in meters')
    setup_args.add_argument('--camera-elevation', '-ce', type=float, default=1,
                            help='Camera elevation in meters from conveyor')

    image_args = parser.add_argument_group('Image arguments')
    image_args.add_argument('--image-width', '-iw', type=int, default=640,
                            help='Image width in pixels')
    image_args.add_argument('--image-height', '-ih', type=int, default=480,
                            help='Image width in pixels')

    renderer_args = parser.add_argument_group('Renderer arguments')
    renderer_args.add_argument('--max-samples', type=int, default=128,
                               help='Max samples to render')
    renderer_args.add_argument('--noise-threshold', type=float, default=0.5,
                               help='Noise threshold renderer parameter')

    args = parser.parse_args()
    if args.n_images > 1 and not args.append_out:
        parser.error('Should use --append-out (-ao) when --n-images (-n) > 1.')
    return args
