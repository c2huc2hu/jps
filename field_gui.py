## Building a field in GUI

# I'm thinking that you would use some button to run a JPS. 

import jps
import pygame

X_MAX, Y_MAX = 800, 600
width, height = 100, 50

field = [[jps.UNINITIALIZED for i in range(height)] for j in range(width)]

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode ((X_MAX, Y_MAX))
    main_surface = pygame.Surface ((X_MAX, Y_MAX))

    button_down = False

    while(True):
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                button_down = True
            elif e.type == pygame.MOUSEBUTTONUP:
                button_down = False

        # Handle mouse interface
        if button_down:
            mousex, mousey = pygame.mouse.get_pos()
            if 0 <= mousex // 5 < width and 0 <= mousey // 5 < height:
                print(mousex // 5, mousey // 5)
                field[mousex // 5][mousey // 5] = jps.OBSTACLE
                pygame.draw.rect(main_surface, 0xFFFFFF, (mousex // 5 * 5, mousey // 5 * 5, 5, 5))
                

        window.blit(main_surface, (0, 0))
        pygame.display.flip()
