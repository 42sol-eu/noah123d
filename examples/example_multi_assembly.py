from noah123d import multi_stl_to_3mf
# Simple assembly
stl_objects = [
    {'path': '../models/multiverse/clip_dual_light.stl', 'count': 8},
    {'path': '../models/multiverse/clip_dual.stl', 'count': 8},
    {'path': '../models/multiverse/tile_2x2_border.stl', 'count': 1}
]

multi_stl_to_3mf(stl_objects, 'printer_kit.3mf', layout_mode='grid')