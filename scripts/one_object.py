import blenderproc as bproc

import sys
from pathlib import Path

# Add project root to PATH
project_root = str(Path.cwd())
if project_root not in sys.path:
    sys.path.append(project_root)


from src.config import parse_args
from src.core.scenes import ConveyorScene
from src.core.lighting import FactoryLighting
from src.core.camera import CameraController
from src.core.placement import SingleObjectPhysicsPlacement
from src.core.pipeline import DataGenerationPipeline


def main():
    args = parse_args()
    bproc.init()

    scene = ConveyorScene(
        conveyor_width=args.conveyor_width,
        conveyor_height=args.conveyor_height
    )
    lighting = FactoryLighting()
    camera = CameraController(
        image_width=args.image_width,
        image_height=args.image_height,
        elevation=args.camera_elevation
    )

    placement_strategy = SingleObjectPhysicsPlacement(
        objects_dir=args.objects_dir,
        object_name=args.object,
        spawn_height=args.conveyor_height + args.camera_elevation,
        strict_center=args.strict_center
    )

    pipeline = DataGenerationPipeline(
        scene=scene,
        lighting=lighting,
        camera=camera,
        placement_strategy=placement_strategy,
        config=args
    )

    pipeline.initialize_blender()
    pipeline.generate_dataset()


if __name__ == '__main__':
    main()
