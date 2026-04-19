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



class Bookmark(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.offset_x = self.rect.x - event.pos[0]
                    self.offset_y = self.rect.y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_dragging = False

        if self.is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y


note_width = int(WIDTH * 0.65)  
note_height = int(HEIGHT * 0.9)
note_x = 0
note_y = (HEIGHT - note_height) // 2
note = Note(os.path.join("materials", "lv1 note.png"), note_width, note_height, note_x, note_y)

bm_width = int(note_width * 0.9)
bm_height = int(note_height * 1.0)
bm = Bookmark(os.path.join("materials", "book mark.png"), 
              bm_width, bm_height, 
              note_x + int(note_width * 0.6), note_y + 50)

all_sprites = pygame.sprite.Group()
all_sprites.add(note)
all_sprites.add(bm)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    bm.update(events)

    screen.blit(background_img, (0, 0))

    all_sprites.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
