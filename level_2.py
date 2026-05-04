def run_level_2(screen):
    import pygame
    import os
    import math
    import time
    
    level_complete = False

    clock = pygame.time.Clock()
    info = pygame.display.Info()
    WIDTH, HEIGHT = 1200, 650
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CYAN = (0, 255, 255)

    background_img = pygame.image.load(os.path.join("materials", "lv1 background.png")).convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


    STARS = [
    # B
        [-320,-100,0], [-320,-50,0], [-320,0,0], [-320,50,0], [-320,100,0],
        [-270,-75,0], [-250,-50,0], [-250,0,0], [-250,50,0], [-270,75,0],

        #C
        [-120,-100,0], [-80,-100,0],
        [-120,100,0], [-80,100,0],

        #F
        [80,-100,0], [80,-50,0], [80,0,0], [80,50,0], [80,100,0],
        [130,-100,0], [130,0,0],

        #I
        [220,-100,0], [220,100,0]
    ]
    OFFSET_X = -300
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


    def rotate_point(point, ax, ay):
        x, y, z = point

        nx = x * math.cos(ay) + z * math.sin(ay)
        nz = -x * math.sin(ay) + z * math.cos(ay)

        ny = y * math.cos(ax) - nz * math.sin(ax)
        nz = y * math.sin(ax) + nz * math.cos(ax)

        return [nx, ny, nz]


    def project(point):
        x, y, z = point
        factor = 600 / (z + 800)
        px = x * factor + WIDTH // 2
        py = y * factor + HEIGHT // 2
        return int(px), int(py), factor

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

                sensitivity = 0.003
                self.angle_y += dx * sensitivity
                self.angle_x += dy * sensitivity
                self.angle_x = max(-math.pi/2, min(math.pi/2, self.angle_x))

                self.last_mouse_pos = event.pos

        def update(self):
            self.image.fill((0, 0, 0, 0))

            rotated = [rotate_point(p, self.angle_x, self.angle_y) for p in STARS]
            projected = [project(p) for p in rotated]

            for i, j in CONNECTIONS:
                pygame.draw.line(
                    self.image,
                    (80, 80, 140),projected[i][:2],projected[j][:2],2)
                
            for x, y, factor in projected:
                size = max(3, int(8 * factor))
                pygame.draw.circle(self.image, WHITE, (x, y), size)

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

    while not level_complete:
        screen_width = 1200
        screen_height = 650
        pygame.display.set_caption("The Puzzle House")

        LIGHT_BLUE = (202, 228, 241)

        screen.fill(LIGHT_BLUE)

        right_section_width = screen_width // 3
        button_area_start_x = screen_width - right_section_width

        images = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        enter_img = pygame.image.load("materials/button/enter.png")
        enter_img = pygame.transform.scale(enter_img, (45, 45))

        for letter in letters:
            img = pygame.image.load(f"materials/button/letter_{letter}.png")
            images[letter] = pygame.transform.scale(img, (45, 45))

        button_size = 45
        button_gap = 80
        buttons_per_row = 3
        rows = 3

        total_grid_width = buttons_per_row * button_gap
        total_grid_height = rows * button_gap

        grid_start_x = button_area_start_x + (right_section_width - total_grid_width) // 2
        grid_start_y = (screen_height - total_grid_height) // 2

        buttons = []
        for i, letter in enumerate(letters):
            row = i // buttons_per_row
            col = i % buttons_per_row
            x = grid_start_x + col * button_gap
            y = grid_start_y + row * button_gap
            btn = Letter_Button(x, y, images[letter])
            btn.letter = letter
            buttons.append(btn)

        enter_btn_x = grid_start_x + (total_grid_width // 2) - 22
        enter_btn_y = grid_start_y + total_grid_height + 30
        enter_btn = Letter_Button(enter_btn_x, enter_btn_y, enter_img)
        enter_btn.letter = "ENTER"
        buttons.append(enter_btn)

        passcode = []
        correct_passcode = ['b', 'c', 'f', 'i']


        all_sprites = pygame.sprite.Group()
        constellation = Constellation()
        all_sprites.add(constellation)

        for btn in buttons:
            btn.draw()

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                constellation.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (clicked_btn := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"),None)):
                        if True:
                            passcode.append(clicked_btn.letter)
                            print(f"Clicked: {clicked_btn.letter}, passcode: {passcode}")
                            clicked_btn.hide()
                    elif (enter_clicked := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"),None)):
                        if passcode == correct_passcode:
                            for btn in buttons:
                                btn.visible = False
                            congratulations = pygame.font.SysFont(None, 70).render("Congratulations!", True, (0, 128, 0))
                            screen.blit(congratulations,(400,305))
                            pygame.display.flip()
                            level_completed = True
                            time.sleep(1)
                            return "complete"
                        else:
                           print(f"❌ Invalid password: {passcode}")
                           for btn in buttons:
                               if btn.letter != "ENTER":
                                   btn.visible = True
                                   btn.clicked = False
                           passcode = []
                           print("Game reset. Try again.")
                constellation.handle_event(event)

            all_sprites.update()

            screen.fill(BLACK)

            screen.blit(background_img, (0, 0))
                
            for btn in buttons:
                if not btn.visible and btn.letter != "ENTER":
                    font = pygame.font.Font(None, 36)
                    check = font.render("", True, (0, 255, 0))
                    screen.blit(check, (btn.rect.centerx - 15, btn.rect.centery - 15))

            all_sprites.draw(screen)

            wall_width = 400
            pygame.draw.rect(screen,WHITE,(WIDTH - wall_width, 0, wall_width, HEIGHT))

            for btn in buttons:
                btn.draw()

            pygame.display.flip()
