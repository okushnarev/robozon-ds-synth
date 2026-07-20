import blenderproc as bproc
import numpy as np

from src.core.scenes import BaseScene
from src.core.lighting import BaseLighting
from src.core.camera import CameraController
from src.core.placement import BasePlacementStrategy


class DataGenerationPipeline:
    def __init__(self,
                 scene: BaseScene,
                 lighting: BaseLighting,
                 camera: CameraController,
                 placement_strategy: BasePlacementStrategy,
                 config):
        self.scene = scene
        self.lighting = lighting
        self.camera = camera
        self.placement_strategy = placement_strategy
        self.config = config

        self.rng = np.random.default_rng(config.seed)
        self._align_rng_state(self.placement_strategy.n_requests_per_render)

    def _align_rng_state(self, n_requests_per_render: int) -> None:
        if self.config.append_out:
            existing_indices = [int(f.stem) for f in self.config.output_dir.glob('*.hdf5') if f.stem.isdigit()]
            if existing_indices:
                max_idx = max(existing_indices)
                self.rng.bit_generator.advance(max_idx * n_requests_per_render)

    def initialize_blender(self) -> None:
        bproc.init()
        self.scene.build()
        self.lighting.setup()
        self.placement_strategy.setup()

        # Renderer configurations
        bproc.renderer.enable_depth_output(activate_antialiasing=False)
        bproc.renderer.enable_segmentation_output(map_by=['category_id'], default_values={'category_id': 0})
        bproc.renderer.set_max_amount_of_samples(self.config.max_samples)
        bproc.renderer.set_noise_threshold(self.config.noise_threshold)

    def generate_dataset(self) -> None:
        cam_pose = self.camera.get_overhead_pose(self.config.conveyor_height)

        for _ in range(self.config.n_images):
            bproc.utility.reset_keyframes()

            # Objects' spatial assignment and simulation
            self.placement_strategy.step(self.rng)

            # Record pose and render
            bproc.camera.add_camera_pose(cam_pose)
            render_data = bproc.renderer.render()

            # Output results
            bproc.writer.write_hdf5(
                self.config.output_dir,
                render_data,
                append_to_existing_output=self.config.append_out
            )