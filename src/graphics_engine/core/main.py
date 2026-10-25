import pygame
from graphics_engine.core.config import config

def main():
    window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), config.SCREEN_FLAGS)
    pygame.display.set_caption("Graphics Engine")

    canvas = pygame.Surface((config.CANVAS_WIDTH, config.CANVAS_HEIGHT))

    clock = pygame.time.Clock()
    running = True

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

        canvas.fill((240, 240, 240))

        center_x = int((config.SCREEN_WIDTH // 2) * config.SCALE)
        center_y = int((config.SCREEN_HEIGHT // 2) * config.SCALE)
        radius = int(50 * config.SCALE)
        line_width = int(5 * config.SCALE)

        pygame.draw.circle(canvas, (30, 144, 255), (center_x, center_y), radius, line_width)
        
        for x in range(0, config.SCREEN_WIDTH * config.SCALE, int(50 * config.SCALE)):
            pygame.draw.line(canvas, (220, 220, 220), (x, 0), (x, config.SCREEN_HEIGHT * config.SCALE), config.SCALE)

        # --- BLITTING & SCALING PHASE ---
        # Scale the massive high-res canvas down to fit the smaller window using smooth scaling
        scaled_canvas = pygame.transform.smoothscale(canvas, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        window.blit(scaled_canvas, (0, 0))

        pygame.display.flip()
        clock.tick(config.FPS_CAP)

    pygame.quit()