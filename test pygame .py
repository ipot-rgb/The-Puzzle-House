<<<<<<< HEAD
import pygame
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("testing testing 123")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

=======
import pygame
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame Test")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

>>>>>>> d57c7e8ae16c094646877c7991c47093acd5065d
pygame.quit()