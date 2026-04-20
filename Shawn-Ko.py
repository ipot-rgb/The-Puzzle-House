import pygame

pygame.init()

screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))

bck_img = pygame.image.load('SK-background.png').convert()
bck_img = pygame.transform.scale(bck_img, (screen_width, screen_height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bck_img, (0,0))

    pygame.display.flip()
pygame.quit()