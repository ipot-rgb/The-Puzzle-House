import pygame

pygame.init()

screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Puzzle House")


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
    screen.blit(brg, (0, 0))
    for p in puzzles:
        screen.blit(p["img"], p["rect"])
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, p in enumerate(puzzles):
                    if p["rect"].collidepoint(event.pos):
                        active_puzzle = i

        elif event.type == pygame.MOUSEBUTTONUP:
            active_puzzle = None

        elif event.type == pygame.MOUSEMOTION:
            if active_puzzle is not None:
                puzzles[active_puzzle]["rect"].move_ip(event.rel)
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()