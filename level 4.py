import pygame
import os

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Level 1")
clock = pygame.time.Clock()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
background_img = pygame.image.load(os.path.join("materials", "lv1 background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_img, (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()