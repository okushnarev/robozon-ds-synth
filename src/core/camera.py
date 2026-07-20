import blenderproc as bproc
import numpy as np


class CameraController:
    """Handles intrinsic and extrinsic settings of the Blender camera."""

    def __init__(
            self,
            image_width: int,
            image_height: int,
            elevation: float,
            base_width: int = 640,
            base_height: int = 480,
            fx: float = 355.0066183,
            fy: float = 355.066183,
            cx: float = 320,
            cy: float = 240,
            s: float = 0,
    ):
        self.image_width = image_width
        self.image_height = image_height
        self.elevation = elevation
        self.base_width = base_width
        self.base_height = base_height

        # Camera params
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.s = s

        self.setup_intrinsics()

    def setup_intrinsics(self, ) -> None:
        s_x = self.image_width / self.base_width
        s_y = self.image_height / self.base_height

        fx = self.fx * s_x
        fy = self.fy * s_y
        cx = self.cx * s_x
        cy = self.cy * s_y

        K = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ])
        bproc.camera.set_intrinsics_from_K_matrix(K, self.image_width, self.image_height)

    def get_overhead_pose(self, scene_height: float) -> np.ndarray:
        """Returns pose matrix pointing straight down at the scene."""
        return bproc.math.build_transformation_mat(
            [0, 0, scene_height + self.elevation],
            [0, 0, 0]
        )
