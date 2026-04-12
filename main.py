import pygame
import time
pygame.init()

# Load images
wall = pygame.image.load("wall.png")
data = open("puzzle_00.png")
data2 = open("puzzle_01.png")
data3 = open("puzzle_02.png")
data4 = open("puzzle_03.png")
puzzle = pygame.image.load(data, '.png')
puzzle2 = pygame.image.load(data2, '.png')
puzzle3 = pygame.image.load(data3, '.png')
puzzle4 = pygame.image.load(data4, '.png')

# Set up the display
display = pygame.display.set_mode((1200, 650), pygame.SCALED) 

# Background and objects
display.blit(wall, (0, 0))
display.blit(puzzle, (100, 100))

font = pygame.font.Font('C:\\Users\\HP\\OneDrive\\Documents\\PythonGame\\OpenSans-VariableFont_wdth,wght.ttf', 36)
text = font.render("Hello, World!", True, (0,0,0))
display.blit(text, (400, 300))

# # Color 
# color = Color(255, 0, 0)  # Red color
# color2 = Color(f"#5F5F5F")  # Gray color
# pygame.draw.rect(display, color, (250,0,0))

# Update the display
pygame.display.flip()

time.sleep(2)

# Quit Pygame
start = pygame.quit()