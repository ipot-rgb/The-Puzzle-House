import pygame
import sys
import random

pygame.init()

class Letter_Button:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.letter = None
        self.visible = True
        self.clicked = False
    
    def draw(self):
        if self.visible:
            screen.blit(self.image, self.rect)
    
    def hide(self):
        self.visible = False
        self.clicked = True

screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Puzzle House")

# Screen background color
LIGHT_BLUE = (202, 228, 241)

screen.fill(LIGHT_BLUE)

# ========== Button Configuration ==========
# Right section dimensions
right_section_width = screen_width // 3
button_area_start_x = screen_width - right_section_width

# Picture loading
images = {}
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

enter_img = pygame.image.load("assets/Button_alphabet/enter.png")
enter_img = pygame.transform.scale(enter_img, (45, 45))

for letter in letters:
    img = pygame.image.load(f"assets/Button_alphabet/letter_{letter}.png")
    images[letter] = pygame.transform.scale(img, (45, 45))

# Configure button grid
button_size = 45
button_gap = 80
buttons_per_row = 3
rows = 3

total_grid_width = buttons_per_row * button_gap
total_grid_height = rows * button_gap

# Letters grid start position (centered in the right section)
grid_start_x = button_area_start_x + (right_section_width - total_grid_width) // 2
grid_start_y = (screen_height - total_grid_height) // 2

# Create letter buttons
buttons = []
for i, letter in enumerate(letters):
    row = i // buttons_per_row
    col = i % buttons_per_row
    x = grid_start_x + col * button_gap
    y = grid_start_y + row * button_gap
    btn = Letter_Button(x, y, images[letter])
    btn.letter = letter
    buttons.append(btn)

# ENTER Button
enter_btn_x = grid_start_x + (total_grid_width // 2) - 22
enter_btn_y = grid_start_y + total_grid_height + 30
enter_btn = Letter_Button(enter_btn_x, enter_btn_y, enter_img)
enter_btn.letter = "ENTER"
buttons.append(enter_btn)

# Passcode variables
passcode = []
correct_passcode = ['a', 'b', 'c', 'd']

# Button Drawing
for btn in buttons:
    btn.draw()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # == Check LETTER button click ==
            if (clicked_btn := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"),None)):
                if True:
                    passcode.append(clicked_btn.letter)
                    print(f"Clicked: {clicked_btn.letter}, passcode: {passcode}")
                    clicked_btn.hide()

            # == Check ENTER button click ==
            # Checking if the click is on the ENTER button and if it's visible (not hidden)
            elif (enter_clicked := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"),None)):
                if True:
                    if passcode == correct_passcode:
                        print("✅ You passed!")
                        
                    else:
                        print(f"❌ Invalid password: {correct_passcode}")
                        # Reset buttons
                        for btn in buttons:
                            if btn.letter != "ENTER":
                                btn.visible = True
                                btn.clicked = False
                        passcode = []
                        print("Game reset. Try again.")
                
    # Srcreen refresh
    screen.fill(LIGHT_BLUE)
    
    # Button drawing
    for btn in buttons:
        btn.draw()
    
    # Disappearing buttons 
    for btn in buttons:
        if not btn.visible and btn.letter != "ENTER":
            font = pygame.font.Font(None, 36)
            check = font.render("", True, (0, 255, 0))
            screen.blit(check, (btn.rect.centerx - 15, btn.rect.centery - 15))
    
    pygame.display.update()

pygame.quit()

