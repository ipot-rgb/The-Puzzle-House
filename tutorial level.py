import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1200,650), pygame.SCALED)
clock = pygame.time.Clock()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

background_img = pygame.image.load(os.path.join("materials", "tutorial level background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_img, (0, 0))
    pygame.display.update()

pygame.quit()