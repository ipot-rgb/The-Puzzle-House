import pygame
import time
pygame.init()

# Load images
wall = pygame.image.load("wall.png")
data = open("puzzle_00.png")
puzzle = pygame.image.load(data, '.png')

# Set up the display
display = pygame.display.set_mode((1200, 700), pygame.SCALED) 

# Update the display
pygame.display.update()

pygame.display.toggle_fullscreen()
time.sleep(2)

# Quit Pygame
pygame.quit()