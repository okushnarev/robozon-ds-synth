import blenderproc as bproc
import numpy as np
from pathlib import Path


class BasePlacementStrategy:
    """Interface for loading, positioning, and simulating target objects."""
    n_requests_per_render: int

    def setup(self) -> None:
        """Called once during initialization to load objects and prepare them."""
        raise NotImplementedError

    def step(self, rng: np.random.Generator) -> None:
        """Called on every iteration to reposition objects and run simulations."""
        raise NotImplementedError


class SingleObjectPhysicsPlacement(BasePlacementStrategy):
    """Original behavior: Loads a single object and drops it onto the conveyor using physics."""
    n_requests_per_render = 3
    def __init__(self, objects_dir: Path, object_name: str, spawn_height: float, strict_center: bool):
        self.objects_dir = objects_dir
        self.object_name = object_name
        self.spawn_height = spawn_height
        self.strict_center = strict_center
        self.target_obj = None

    def setup(self) -> None:
        blend_file = self.objects_dir / f'{self.object_name}.blend'
        self.target_obj = bproc.loader.load_blend(str(blend_file))[0]
        self.target_obj.set_cp('category_id', 1)
        self.target_obj.enable_rigidbody(active=True)

    def step(self, rng: np.random.Generator) -> None:
        self.target_obj.set_location([0, 0, self.spawn_height])
        self.target_obj.set_rotation_euler(rng.uniform(0, 2 * np.pi, 3))

        bproc.object.simulate_physics_and_fix_final_poses(
            min_simulation_time=4,
            max_simulation_time=20,
            check_object_interval=2
        )

        if self.strict_center:
            current_z = self.target_obj.get_location()[2]
            self.target_obj.set_location([0, 0, current_z])
