from pydantic_settings import BaseSettings
import pygame

pygame.init()
info = pygame.display.Info()

class Configs(BaseSettings):
    SCREEN_WIDTH: int = info.current_w
    SCREEN_HEIGHT: int = info.current_h
    SCREEN_FLAGS: int =  pygame.FULLSCREEN | pygame.NOFRAME
    SCALE: int = 2

    CANVAS_WIDTH: int = SCREEN_WIDTH * SCALE
    CANVAS_HEIGHT: int = SCREEN_HEIGHT * SCALE
    
    FPS_CAP: int = 30

config = Configs()