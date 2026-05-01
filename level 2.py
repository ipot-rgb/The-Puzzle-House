import pygame
import os
import math

pygame.init()
screen = pygame.display.set_mode((1200,650), pygame.SCALED)
clock = pygame.time.Clock()
info = pygame.display.Info()
WIDTH, HEIGHT = 1200, 650


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# ================== 背景 ==================
background_img = pygame.image.load(
    os.path.join("materials", "lv1 background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# ================== 星座数据 ==================

STARS = [
   # ===== B =====
    [-320,-100,0], [-320,-50,0], [-320,0,0], [-320,50,0], [-320,100,0],
    [-270,-75,0], [-250,-50,0], [-250,0,0], [-250,50,0], [-270,75,0],

    # ===== C =====
    [-120,-100,0], [-80,-100,0],
    [-120,100,0], [-80,100,0],

    # ===== F =====
    [80,-100,0], [80,-50,0], [80,0,0], [80,50,0], [80,100,0],
    [130,-100,0], [130,0,0],

    # ===== I =====
    [220,-100,0], [220,100,0]
]
OFFSET_X = -150
STARS = [[x + OFFSET_X, y, z] for x, y, z in STARS]

CONNECTIONS = [
    # B
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,2),
    (2,7),(7,8),(8,4),

    # C
    (10,11),
    (10,12),
    (12,13),

    # F
    (14,15),(15,16),(16,17),(17,18),
    (14,19),
    (16,20),

    # I
    (21,22)
]


# ================== 数学函数 ==================
def rotate_point(point, ax, ay):
    x, y, z = point

    # 绕 Y 轴
    nx = x * math.cos(ay) + z * math.sin(ay)
    nz = -x * math.sin(ay) + z * math.cos(ay)

    # 绕 X 轴
    ny = y * math.cos(ax) - nz * math.sin(ax)
    nz = y * math.sin(ax) + nz * math.cos(ax)

    return [nx, ny, nz]


def project(point):
    x, y, z = point
    factor = 600 / (z + 800)
    px = x * factor + WIDTH // 2
    py = y * factor + HEIGHT // 2
    return int(px), int(py), factor

# ================== Sprite ==================
class Constellation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.angle_x = 1.0
        self.angle_y = 1.0
        self.dragging = False
        self.last_mouse_pos = None

        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.last_mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            self.last_mouse_pos = None

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]

            sensitivity = 0.005
            self.angle_y += dx * sensitivity
            self.angle_x += dy * sensitivity

            self.last_mouse_pos = event.pos

    def update(self):
        self.image.fill((0, 0, 0, 0))

        rotated = [rotate_point(p, self.angle_x, self.angle_y) for p in STARS]
        projected = [project(p) for p in rotated]

        # 画线
        for i, j in CONNECTIONS:
            pygame.draw.line(
                self.image,
                (80, 80, 140),
                projected[i][:2],
                projected[j][:2],
                2
            )

        # 画星点
        for x, y, factor in projected:
            size = max(3, int(8 * factor))
            pygame.draw.circle(self.image, WHITE, (x, y), size)


# ================== 主循环 ==================
all_sprites = pygame.sprite.Group()
constellation = Constellation()
all_sprites.add(constellation)


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        constellation.handle_event(event)

    all_sprites.update()

    screen.fill(BLACK)

    screen.blit(background_img, (0, 0))

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()


