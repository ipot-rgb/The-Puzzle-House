import pygame
import time
pygame.init()

# Load images
wall = pygame.image.load("wall.png")
data = open("puzzle_00.png")
puzzle = pygame.image.load(data, '.png')

# Set up the display screen
display = pygame.display.set_mode((1200, 650), pygame.SCALED) 
icon = pygame.image.load("puzzle_icon.png")
pygame.display.set_icon(icon)

# Background and objects
display.blit(wall, (0, 0))
display.blit(puzzle, (100, 100))

font = pygame.font.Font('C:\\Users\\HP\\OneDrive\\Documents\\PythonGame\\OpenSans-VariableFont_wdth,wght.ttf', 36)
text = font.render("Hello, World!", True, (0,0,0))
display.blit(text, (400, 300))

# Update the display
pygame.display.flip()

time.sleep(2)
text_1 = font.render("This is other screen", False, (0,0,0))
display.blit(text_1, (400, 300))
wall2 = pygame.image.load("background.png")
wall2 = pygame.transform.scale(wall2, (1200, 650))
display.blit(wall2, (0, 0))
pygame.display.update()

time.sleep(2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
