import blenderproc as bproc
import numpy as np

class BaseLighting:
    """Base class for lighting strategies."""
    def setup(self) -> None:
        raise NotImplementedError('Each lighting strategy must implement the setup method.')

class AmbientLighting(BaseLighting):
    """The dual area light setup with ambient sunlight and factory like lamps"""
    def setup(self) -> None:
        # Create ambient light
        self.sun = bproc.types.Light('SUN', 'ambient')
        self.sun.blender_obj.data.use_shadow = False
        self.sun.blender_obj.data.angle = np.deg2rad(90)
        self.sun.set_energy(10)

class ConveyorLighting(AmbientLighting):
    """The dual area light setup with ambient sunlight and factory like lamps"""
    def setup(self) -> None:
        super().setup()
        # Create local lights
        self.light_top = bproc.types.Light('AREA', 'light_top')
        self.light_top.blender_obj.data.shape = 'RECTANGLE'
        self.light_top.blender_obj.data.size = 0.6
        self.light_top.blender_obj.data.size_y = 0.3
        self.light_top.set_location([0, 0.7, 1.4])
        self.light_top.set_rotation_euler([np.deg2rad(-45), 0, 0])
        self.light_top.set_energy(10)

        self.light_bot = bproc.types.Light('AREA', 'light_bot')
        self.light_bot.blender_obj.data.shape = 'RECTANGLE'
        self.light_bot.blender_obj.data.size = 0.6
        self.light_bot.blender_obj.data.size_y = 0.3
        self.light_bot.set_location([0, -0.7, 1.4])
        self.light_bot.set_rotation_euler([np.deg2rad(45), 0, 0])
        self.light_bot.set_energy(10)