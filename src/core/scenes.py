import blenderproc as bproc
import numpy as np


class BaseScene:
    """Base class for environment scenes."""

    def build(self) -> None:
        raise NotImplementedError('Each scene must implement the build method.')


class ConveyorScene(BaseScene):
    """Conveyor belt environment with side walls."""

    def __init__(self, conveyor_width: float, conveyor_height: float):
        self.width = conveyor_width
        self.height = conveyor_height

    def build(self) -> None:
        # Ground
        ground_mat = bproc.material.create('Ground')
        ground_mat.set_principled_shader_value('Base Color', [0.8, 0.8, 0.8, 1.0])

        ground = bproc.object.create_primitive('PLANE')
        ground.replace_materials(ground_mat)
        ground.set_scale([10, 10, 1])
        ground.set_location([0, 0, 0])
        ground.enable_rigidbody(active=False)

        # Conveyor
        conv_mat = bproc.material.create('Conveyor')
        conv_mat.set_principled_shader_value('Base Color', [0.04, 0.04, 0.04, 1.0])
        conv_mat.set_principled_shader_value('Roughness', 0.6)

        conveyor = bproc.object.create_primitive('PLANE')
        conveyor.replace_materials(conv_mat)
        conveyor.set_scale([10, self.width / 2, 1])
        conveyor.set_location([0, 0, self.height])
        conveyor.enable_rigidbody(active=False, collision_shape='MESH')

        # Invisible side walls
        self._build_walls()

    def _build_walls(self) -> None:
        wall_top = bproc.object.create_primitive('PLANE')
        wall_top.set_scale([10, 10, 10])
        wall_top.set_location([0, self.width / 2, self.height])
        wall_top.set_rotation_euler([np.deg2rad(80), 0, 0])
        wall_top.enable_rigidbody(active=False)
        wall_top.hide()

        wall_bot = bproc.object.create_primitive('PLANE')
        wall_bot.set_scale([10, 10, 10])
        wall_bot.set_location([0, -self.width / 2, self.height])
        wall_bot.set_rotation_euler([np.deg2rad(-80), 0, 0])
        wall_bot.enable_rigidbody(active=False)
        wall_bot.hide()