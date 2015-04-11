from jps import *

set_visual(True)

# Image test to load a map from an image
m = load_path_image('toronto.png', 0x00ffff)
print("loaded image")
path = get_full_path(jps(m, 40, 20, 607, 310))  # calculate a path from (40, 20) to (607, 310). 
print("calculated shortest path")
draw_jps(m, path, 'toronto.png')
