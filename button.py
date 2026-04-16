import pygame
pygame.init()

screen = pygame.display.set_mode((1200, 650))
pygame.display.set_caption("The Puzzle House")
icon = pygame.image.load("assets/Icon/puzzle_icon.png")
pygame.display.set_icon(icon)
pygame.display.update()

class Letter_Button:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self):
        screen.blit(self.image, self.rect)

screen.fill((202, 228, 241))
letters = ["a","b","c","d","e","f","g","h","i"]

images = {}
for letter in letters:
    enter_img = pygame.image.load("assets/Button_alphabet/enter.png")
    enter_img = pygame.transform.scale(enter_img, (45,45))


buttons = []

start_x = 100
start_y = 100
gap = 80

for i, letter in enumerate(letters):
    img = pygame.image.load(f"assets/Button_alphabet/letter_{letter}.png")
    images[letter] = pygame.transform.scale(img, (45,45))
    enter_btn = Letter_Button(1000, 100, enter_img)
    enter_btn.letter = "ENTER"
    x = start_x + (i % 3) * gap   # 每3个换行
    y = start_y + (i // 3) * gap

    btn = Letter_Button(x, y, images[letter])
    btn.letter = letter
    buttons.append(btn)
buttons.append(enter_btn)
for btn in buttons:
    btn.draw()

running = True
while running: 
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in buttons:
                if btn.rect.collidepoint(event.pos):
                    print("clicked:", btn.letter)
                
    pygame.display.update()
pygame.quit()