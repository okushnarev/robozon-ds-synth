import blenderproc as bproc
import numpy as np

class BaseLighting:
    """Base class for lighting strategies."""
    def setup(self) -> None:
        raise NotImplementedError('Each lighting strategy must implement the setup method.')


class ConveyorLighting(BaseLighting):
    """The dual area light setup with ambient sunlight and factory like lamps"""
    def setup(self) -> None:
        # Create ambient light
        sun = bproc.types.Light('SUN')
        sun.blender_obj.data.use_shadow = False
        sun.blender_obj.data.angle = np.deg2rad(90)
        sun.set_energy(10)

        # Create local lights
        light_top = bproc.types.Light('AREA', 'light_top')
        light_top.blender_obj.data.shape = 'RECTANGLE'
        light_top.blender_obj.data.size = 0.6
        light_top.blender_obj.data.size_y = 0.3
        light_top.set_location([0, 0.7, 1.4])
        light_top.set_rotation_euler([np.deg2rad(-45), 0, 0])
        light_top.set_energy(10)

        light_bot = bproc.types.Light('AREA', 'light_bot')
        light_bot.blender_obj.data.shape = 'RECTANGLE'
        light_bot.blender_obj.data.size = 0.6
        light_bot.blender_obj.data.size_y = 0.3
        light_bot.set_location([0, -0.7, 1.4])
        light_bot.set_rotation_euler([np.deg2rad(45), 0, 0])
        light_bot.set_energy(10)