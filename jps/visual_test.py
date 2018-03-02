# Randomly generate obstacles on a field, and display the output using pygame.


from jps import *
import random

DENSITY = 5  # Percentage of the field that is filled. 

set_visual(True) 

if DEBUG:
    import cProfile, time
    pr = cProfile.Profile()
    t = time.time()

raw_field = [[random.randint(0, 100) for i in range(150)] for j in range(200)]
field = generate_field(raw_field, (lambda cell: True if cell > DENSITY else False), True)
field[1][1] = UNINITIALIZED  # guarantee that the end is reachable
field[198][148] = UNINITIALIZED 

if DEBUG:
    print("took ", time.time() - t, " to generate field")
    t = time.time()
    pr.enable() # start the profiler
    
path = jps(field, 1, 1, 198, 148)
path = get_full_path(path)

if DEBUG:
    pr.disable()
    print("took ", (time.time() - t), " to do search")
    t = time.time()
    print("full long path: ", path)
    pr.print_stats() 

if VISUAL:
    try:
        draw_jps(field, path)
    except ImportError as err:
        print("You don't have pygame. Cannot display large test. ", err)
else:
    print("Visual is turned off") 
