import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1200,650), pygame.SCALED)
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1200, 650
offset_y=120
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_img = pygame.image.load(os.path.join("materials", "tutorial level background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

class puzzle(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class puzzle_piece_one(pygame.sprite.Sprite):
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


class puzzle_piece_two(pygame.sprite.Sprite):
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


class puzzle_piece_three(pygame.sprite.Sprite):
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

class puzzle_piece_four(pygame.sprite.Sprite):
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


puzzle_width = int(WIDTH * 0.6)  
puzzle_height = int(HEIGHT * 1.0)
puzzle_x = 0
puzzle_y = (HEIGHT - puzzle_height) // 2
puzzle = puzzle(os.path.join("materials", "puzzle", "puzzle.png"), puzzle_width, puzzle_height, puzzle_x, puzzle_y)

ppo_width = int(puzzle_width * 0.35)
ppo_height = int(puzzle_height * 0.35)
ppo = puzzle_piece_one(os.path.join("materials", "puzzle", "puzzle piece(1).png"), ppo_width, ppo_height, puzzle.rect.right + 40, puzzle.rect.top + 80)

ppt_width = int(puzzle_width * 0.35)
ppt_height = int(puzzle_height * 0.35)
ppt = puzzle_piece_two(os.path.join("materials", "puzzle", "puzzle piece(2).png"), ppt_width, ppt_height, ppo.rect.x , ppo.rect.y + offset_y)

ppth_width = int(puzzle_width * 0.30)
ppth_height = int(puzzle_height * 0.30)
ppth = puzzle_piece_three(os.path.join("materials", "puzzle", "puzzle piece(3).png"), ppth_width, ppth_height, ppt.rect.x , ppt.rect.y + offset_y)

ppf_width = int(puzzle_width * 0.60)
ppf_height = int(puzzle_height * 0.60)
ppf= puzzle_piece_four(os.path.join("materials", "puzzle", "puzzle piece(4).png"), ppf_width, ppf_height, ppth.rect.x , ppth.rect.y + offset_y)

all_sprites = pygame.sprite.Group()
all_sprites.add(puzzle)
all_sprites.add(ppo)
all_sprites.add(ppt)
all_sprites.add(ppth)
all_sprites.add(ppf)

running = True
while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(events)

    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.update()

screen.blit(background_img, (0, 0))
all_sprites.draw(screen)
pygame.display.update()

pygame.quit()