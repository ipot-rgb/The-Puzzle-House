import pygame
import time

pygame.init()
#===============================
# Main Menu
#===============================
display = pygame.display.set_mode((1200, 650), pygame.SCALED) 
exit_icon = pygame.image.load("exit_button.png")
exit_icon = pygame.transform.scale(exit_icon, (110, 75))
pygame.display.flip()

#===============================
# Set up the display screen
#===============================
pygame.display.set_caption("The Puzzle House")
icon = pygame.image.load("puzzle_icon.png")
pygame.display.set_icon(icon)

#===============================
# Button class
#===============================
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, display):
        display.blit(self.image, self.rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

#===============================
# Picture class
#===============================
class picture:
    def __init__(self, image_name, x, y):
        self.name = pygame.image.load(image_name)
        self.x = x
        self.y = y

brg = picture("menu_brg.jpg", 0, 0)
display.blit(brg.name, (brg.x, brg.y))

exit_button = Button(1125, 587, exit_icon)

default_cursor = pygame.SYSTEM_CURSOR_ARROW
hand_cursor = pygame.SYSTEM_CURSOR_HAND


#===============================
# Game loop
#===============================
running = True
while running:
    exit_button.update(display)

    #cursor changing
    mouse_pos = pygame.mouse.get_pos()
    if exit_button.is_hovered(mouse_pos):
        pygame.mouse.set_cursor(hand_cursor)
    else:
        pygame.mouse.set_cursor(default_cursor)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event.pos):
                running = False

    pygame.display.update()
pygame.quit()


# # Load images
# wall = pygame.image.load("wall.png")
# data = open("puzzle_00.png")
# puzzle = pygame.image.load(data, '.png')


# # Background and objects
# display.blit(wall, (0, 0))
# display.blit(puzzle, (100, 100))

# font = pygame.font.Font('C:\\Users\\HP\\OneDrive\\Documents\\PythonGame\\OpenSans-VariableFont_wdth,wght.ttf', 36)
# text = font.render("Hello, World!", True, (0,0,0))
# display.blit(text, (400, 300))

# # Update the display
# pygame.display.flip()

# time.sleep(2)
# text_1 = font.render("This is other screen", True, (0,0,0))
# display.blit(text_1, (0,0))
# wall2 = pygame.image.load("background.png")
# wall2 = pygame.transform.scale(wall2, (1000, 650))
# display.blit(wall2, (0, 0))
# pygame.display.flip()

# time.sleep(2)