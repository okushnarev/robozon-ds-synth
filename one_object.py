import blenderproc as bproc

from argparse import ArgumentParser
from pathlib import Path
import numpy as np



def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--object', type=str, default='bottle',
                        help='Name of the .blend object. Object should be single in the .blend file. The first object from .blend file is used')

    parser.add_argument('--objects-dir', type=Path, default=Path('input/blend'), help='Directory with .blend objects')
    parser.add_argument('--output-dir', '-od', type=Path, default=Path('output'), help='Directory to output .hdf5 files')
    parser.add_argument('--append-out', '-ao', action='store_true', help='Auto append frame name in out folder')
    parser.add_argument('--seed', type=int, default=69, help='Seed for random number generator')

    setup_args = parser.add_argument_group('Setup arguments')
    setup_args.add_argument('--conveyor-height', '-ch', type=float, default=0.7,
                        help='Conveyor height in meters from ground')
    setup_args.add_argument('--conveyor-width', '-cw', type=float, default=0.5,
                        help='Conveyor width in meters')
    setup_args.add_argument('--camera-elevation', '-ce', type=float, default=1,
                        help='Camera elevation in meters from conveyor')

    image_args = parser.add_argument_group('Image arguments')
    image_args.add_argument('--image-width', '-iw', type=int, default=1920, help='Image width in pixels')
    image_args.add_argument('--image-height', '-ih', type=int, default=1440, help='Image width in pixels')

    renderer_args = parser.add_argument_group('Renderer arguments')
    renderer_args.add_argument('--max-samples', type=int, default=128, help='Max samples to render')
    renderer_args.add_argument('--noise-threshold', type=float, default=0.5, help='Noise threshold renderer parameter')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    bproc.init()

    # Ground material
    ground_mat = bproc.material.create('Ground')
    ground_mat.set_principled_shader_value('Base Color', [0.8, 0.8, 0.8, 1.0])

    # Create ground
    ground = bproc.object.create_primitive('PLANE')
    ground.replace_materials(ground_mat)
    ground.set_scale([10, 10, 1])
    ground.set_location([0, 0, 0])
    ground.enable_rigidbody(active=False)

    # Conveyor material
    conv_mat = bproc.material.create('Conveyor')
    conv_mat.set_principled_shader_value('Base Color', [0.04, 0.04, 0.04, 1.0])
    conv_mat.set_principled_shader_value('Roughness', 0.6)

    # Create conveyor
    conveyor = bproc.object.create_primitive('PLANE')
    conveyor.replace_materials(conv_mat)
    conveyor.set_scale([10, args.conveyor_width / 2, 1])
    conveyor.set_location([0, 0, args.conveyor_height])
    conveyor.enable_rigidbody(active=False, collision_shape='MESH')

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

    # Load object
    obj = bproc.loader.load_blend(args.objects_dir / f'{args.object}.blend')[0]
    obj.set_cp('category_id', 1) # Use category_id > 0 to appear is segmap. 0 is background
    obj.enable_rigidbody(active=True)

    # Camera params
    s_x = args.image_width / 640  # base width
    s_y = args.image_height / 480  # base height

    fx = 355.0066183 * s_x
    fy = 355.066183 * s_y
    cx = 320 * s_x
    cy = 240 * s_y
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    bproc.camera.set_intrinsics_from_K_matrix(K, args.image_width, args.image_height)

    # Set the camera to be in front of the object
    cam_pose = bproc.math.build_transformation_mat([0, 0, args.conveyor_height + args.camera_elevation], [0, 0, 0])
    # Set camera pose
    bproc.camera.add_camera_pose(cam_pose)

    # Render params
    bproc.renderer.enable_depth_output(activate_antialiasing=False)
    bproc.renderer.enable_segmentation_output(map_by=['category_id'], default_values={'category_id': 0})
    bproc.renderer.set_max_amount_of_samples(args.max_samples)
    bproc.renderer.set_noise_threshold(args.noise_threshold)

    rng = np.random.default_rng(args.seed)

    obj.set_location([0, 0, args.conveyor_height + args.camera_elevation])
    obj.set_rotation_euler(rng.uniform(0, 2 * np.pi, 3))

    # Run simulation
    bproc.object.simulate_physics_and_fix_final_poses(min_simulation_time=4, max_simulation_time=20,
                                                      check_object_interval=2)
    # Return object to center
    obj.set_location([0, 0, obj.get_location()[2]])

    # Render
    data = bproc.renderer.render()

    # Write the rendering into an hdf5 file
    bproc.writer.write_hdf5(args.output_dir, data, append_to_existing_output=args.append_out)
