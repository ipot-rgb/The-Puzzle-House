import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1200,650), pygame.SCALED)
pygame.display.set_caption("Level 1")
clock = pygame.time.Clock()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# background
background_img = pygame.image.load(os.path.join("materials", "lv1 background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# sprite class for the note
class Note(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

note_width = int(WIDTH * 0.65)  
note_height = int(HEIGHT * 1.1)
note = Note(os.path.join("materials", "lv1 note.png"), note_width, note_height, 0, (HEIGHT - note_height)//2)

all_sprites = pygame.sprite.Group()
all_sprites.add(note)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_img, (0, 0))

    all_sprites.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
