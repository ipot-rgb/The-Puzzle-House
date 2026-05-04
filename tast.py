import pygame
import math

WIDTH, HEIGHT = 1000, 600
BLACK = (5, 5, 15)
WHITE = (255, 255, 255)
GOLD  = (255, 215, 0)
CYAN  = (0, 255, 255)

pygame.init()
screen = pygame.display.set_mode((1200,650), pygame.SCALED)
clock = pygame.time.Clock()
info = pygame.display.Info()
WIDTH, HEIGHT = 1200, 650


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Constellation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stars = [
            # Y
            [-250, -100, 40], [-200, -50, -60], [-150, -100, 20], [-200, 0, 50], [-200, 80, -30],
            # O
            [-50, -80, 10], [50, -80, -40], [50, 80, 60], [-50, 80, -20], [-50, -80, 10], 
            # N
            [150, 80, 30], [150, -80, -50], [250, 80, 10], [250, -80, 40],
            # G
            [450, -80, -20], [350, -80, 50], [350, 80, -40], [450, 80, 10], [450, 0, -60], [400, 0, 30]]


# Specific connections to draw the letters clearly
connections = [
    (0,1), (1,2), (1,3), (3,4),           # Y
    (5,6), (6,7), (7,8), (8,5),           # O
    (10,11), (11,12), (12,13),            # N
    (14,15), (15,16), (16,17), (17,18), (18,19) # G
]

def rotate_point(point, angle_x, angle_y):
    x, y, z = point
    # Y-axis rotation
    nx = x * math.cos(angle_y) + z * math.sin(angle_y)
    nz = -x * math.sin(angle_y) + z * math.cos(angle_y)
    # X-axis rotation
    ny = y * math.cos(angle_x) - nz * math.sin(angle_x)
    nz = y * math.sin(angle_x) + nz * math.cos(angle_x)
    return [nx, ny, nz]

def project(point):
    x, y, z = point
    factor = 600 / (z + 800)
    px = x * factor + WIDTH // 2
    py = y * factor + HEIGHT // 2
    return (int(px), int(py)), factor

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Constellation Puzzle: YONG")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)
    
    # Starting messy rotation
    angle_x, angle_y = 1.0, 1.0
    solved = False
    constellation = Constellation()

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

        # Interaction
        if pygame.mouse.get_pressed()[0]:
            rel_x, rel_y = pygame.mouse.get_rel()
            angle_y += rel_x * 0.005
            angle_x -= rel_y * 0.005
        else:
            pygame.mouse.get_rel()

        # Check Win Condition (near 0, 2PI, 4PI etc.)
        dist_x = min(abs(angle_x % (2*math.pi)), abs(2*math.pi - (angle_x % (2*math.pi))))
        dist_y = min(abs(angle_y % (2*math.pi)), abs(2*math.pi - (angle_y % (2*math.pi))))
        solved = dist_x < 0.12 and dist_y < 0.12

        # Logic & Drawing
        rotated = [rotate_point(p, angle_x, angle_y) for p in constellation.stars]
        projected = [project(p) for p in rotated]
        color = GOLD if solved else WHITE
        line_color = (60, 60, 100) if not solved else (100, 100, 200)

        # Draw Lines
        for conn in connections:
            start_pos = projected[conn[0]][0]
            end_pos = projected[conn[1]][0]
            pygame.draw.line(screen, line_color, start_pos, end_pos, 2)

        # Draw Stars
        for i, (pos, factor) in enumerate(projected):
            size = max(3, int(8 * factor))
            pygame.draw.circle(screen, color, pos, size)
            if solved: pygame.draw.circle(screen, WHITE, pos, size+2, 1)

        # UI
        msg = "Rotate to align the stars..." if not solved else "PASSWORD UNLOCKED: YONG"
        text = font.render(msg, True, CYAN if solved else WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 30))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
