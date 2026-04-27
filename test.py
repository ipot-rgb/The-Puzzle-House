import pygame
pygame.init()

# =========================
# Setup
# =========================
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Puzzle")

FONT = pygame.font.SysFont("arial", 40)
SMALL_FONT = pygame.font.SysFont("arial", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GOLD = (200, 170, 50)
GREEN = (50, 200, 100)
RED = (200, 50, 50)

# =========================
# Initial scrambled tiles
# =========================
grid = [
    [5, 2, 9],
    [4, 7, 1],
    [8, 3, 6]
]

selected = None

# =========================
# Draw Grid
# =========================
def draw_grid():
    for r in range(3):
        for c in range(3):
            x = 150 + c * 100
            y = 150 + r * 100
            rect = pygame.Rect(x, y, 80, 80)

            pygame.draw.rect(screen, GOLD, rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, rect, 3, border_radius=10)

            num = FONT.render(str(grid[r][c]), True, BLACK)
            screen.blit(num, (x + 25, y + 15))

            if selected == (r, c):
                pygame.draw.rect(screen, GREEN, rect, 4, border_radius=10)

# =========================
# Rotate CCW (逆时针90°)
# =========================
def rotate_ccw(g):
    return [list(row) for row in zip(*g)][::-1]

# =========================
# Get clicked cell
# =========================
def get_cell(pos):
    mx, my = pos
    for r in range(3):
        for c in range(3):
            x = 150 + c * 100
            y = 150 + r * 100
            if pygame.Rect(x, y, 80, 80).collidepoint(mx, my):
                return (r, c)
    return None

# =========================
# Check password
# =========================
def check_win():
    return grid[2] == [6, 7, 2]

# =========================
# Buttons
# =========================
rotate_btn = pygame.Rect(150, 500, 130, 50)
check_btn = pygame.Rect(320, 500, 130, 50)

# =========================
# Game Loop
# =========================
running = True
won = False

while running:
    screen.fill((20, 20, 20))

    # Title
    title = SMALL_FONT.render("逆行其踪，得脱逃之数", True, WHITE)
    screen.blit(title, (160, 50))

    draw_grid()

    # Draw buttons
    pygame.draw.rect(screen, WHITE, rotate_btn)
    pygame.draw.rect(screen, WHITE, check_btn)

    screen.blit(SMALL_FONT.render("Rotate", True, BLACK), (165, 510))
    screen.blit(SMALL_FONT.render("Check", True, BLACK), (345, 510))

    # Win text
    if won:
        win_text = FONT.render("ESCAPED!", True, GREEN)
        screen.blit(win_text, (180, 600))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # Click grid
            cell = get_cell(pos)
            if cell:
                if selected is None:
                    selected = cell
                else:
                    r1, c1 = selected
                    r2, c2 = cell

                    # swap
                    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
                    selected = None

            # Rotate button
            elif rotate_btn.collidepoint(pos):
                grid = rotate_ccw(grid)

            # Check button
            elif check_btn.collidepoint(pos):
                if check_win():
                    print("✅ ESCAPED!")
                    won = True
                else:
                    print("❌ Wrong!")

    pygame.display.flip()

pygame.quit()