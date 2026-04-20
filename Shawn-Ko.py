import pygame

pygame.init()

#Screen
screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()

#colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

#Background Image
bck_img = pygame.image.load('SK-Assets/SK-background.png').convert()
bck_img = pygame.transform.scale(bck_img, (screen_width, screen_height))

#grid image
grid_img = pygame.image.load('SK-Assets/SK-grid.png').convert()
grid_img = pygame.transform.scale(grid_img, (screen_width//3, screen_height//2))
grid_img_rect = grid_img.get_rect()
grid_img_rect.bottomright = screen_rect.bottomright
grid_img_width = grid_img.get_width()
grid_img_height = grid_img.get_height()

#creating button for each alphabet
image_x = screen_width - grid_img_width
image_y = screen_height - grid_img_height
cell_width = grid_img_width // 3
cell_height = grid_img_height // 3
buttons = []
for row in range(3):
    for col in range(3):
        number = row * 3 + col + 1
        button_x = image_x + (col * cell_width)
        button_y = image_y + (row * cell_height)
        buttons.append([button_x, button_y, cell_width, cell_height, number, False])

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for button in buttons:
        x, y, width, height, number, hovered = button
        if (x < mouse_x < x + width) and (y < mouse_y < y + height):
            button[5] = True
        else:
            button[5] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                x, y, width, height, number, hovered = button
                if (x < mouse_x < x + width) and (y < mouse_y < y + height):
                    print(f"Button {number} clicked!")

    screen.blit(bck_img, (0,0))
    screen.blit(grid_img, grid_img_rect)
    pygame.display.flip()
pygame.quit()