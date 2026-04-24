import pygame

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

#===============================
# Screen Setup
#===============================
screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Puzzle House")
red = (91, 14, 45)


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



brg = pygame.image.load("assets/Level_15/brg_15.png")
brg = pygame.transform.scale(brg, (screen_width, screen_height))
puzzles = []
for i in range(1, 10):
    img = pygame.image.load(f"assets/Level_15/num_{i}.png")
    img = pygame.transform.scale(img, (100, 100))

    rect = img.get_rect(topleft=(80 * i, 75))
    puzzles.append({"img": img, "rect": rect})

active_puzzle = None
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 按钮点击
            if (clicked_btn := next((btn for btn in buttons 
                if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"), None)):
                
                passcode.append(clicked_btn.letter)
                clicked_btn.hide()

            elif (enter_clicked := next((btn for btn in buttons 
                if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"), None)):
                
                if passcode == correct_passcode:
                    print("✅ You passed!")
                else:
                    for btn in buttons:
                        if btn.letter != "ENTER":
                            btn.visible = True
                    passcode = []

            elif event.button == 1:
                for i, p in enumerate(puzzles):
                    if p["rect"].collidepoint(event.pos):
                        active_puzzle = i

        elif event.type == pygame.MOUSEBUTTONUP:
                active_puzzle = None

        elif event.type == pygame.MOUSEMOTION:
                if active_puzzle is not None:
                    puzzles[active_puzzle]["rect"].move_ip(event.rel)

    screen.blit(brg, (0, 0))
    pygame.draw.rect(screen, red, (830, 0, screen_width - 830, screen_height))
    for btn in buttons:
        btn.draw()
    for p in puzzles:
        screen.blit(p["img"], p["rect"])
    pygame.display.flip()
pygame.quit()