import pygame
from graphics_engine.core.config import config

# 2. Define your scaling factor (2x or 4x)
SCALE = 2  # Set to 4 for quadruple resolution

# 3. Create the actual display window at the base logical size
window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), config.SCREEN_FLAGS)
pygame.display.set_caption("High-Res Pygame Vector Scaling")

# 4. Create a hidden "canvas" surface that is 2x or 4x larger
canvas = pygame.Surface((config.SCREEN_WIDTH * SCALE, config.SCREEN_HEIGHT * SCALE))

clock = pygame.time.Clock()
running = True
x_pos = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                exit()

    # --- DRAWING PHASE ---
    # Fill the high-res canvas with a background color
    canvas.fill((240, 240, 240))

    # IMPORTANT: Multiply all your coordinates, radiuses, and line widths by SCALE!
    # If you want a circle at logical center (400, 300) with radius 50:
    center_x = int((config.SCREEN_WIDTH // 2) * SCALE + x_pos)
    center_y = int((config.SCREEN_HEIGHT // 2) * SCALE)
    radius = int(50 * SCALE)
    line_width = int(5 * SCALE)

    # Draw a crisp, smooth vector-like circle on the high-res canvas
    pygame.draw.circle(canvas, (30, 144, 255), (center_x, center_y), radius, line_width)
    
    # Draw high-res grid lines
    for x in range(0, config.SCREEN_WIDTH * SCALE, int(50 * SCALE)):
        pygame.draw.line(canvas, (220, 220, 220), (x, 0), (x, config.SCREEN_HEIGHT * SCALE), int(SCALE))

    # --- BLITTING & SCALING PHASE ---
    # Scale the massive high-res canvas down to fit the smaller window using smooth scaling
    scaled_canvas = pygame.transform.smoothscale(canvas, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    
    # Blit the smoothed result onto the actual display window
    window.blit(scaled_canvas, (0, 0))

    pygame.display.flip()
    clock.tick(30)

    x_pos += 1

pygame.quit()