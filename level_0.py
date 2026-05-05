def run_level_0(screen, hint_manager):
    import pygame
    import os
    import time

    level_complete = False
    screen = pygame.display.set_mode((1200,650), pygame.SCALED)
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 1200, 650
    screen_width, screen_height = WIDTH, HEIGHT
    offset_y=120
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    background_img = pygame.image.load(os.path.join("materials", "tutorial level background.png")).convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

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

    class puzzle(pygame.sprite.Sprite):
        def __init__(self, image_path, width, height, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    class puzzle_piece_one(pygame.sprite.Sprite):
        def __init__(self, image_path, width, height, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))

            self.is_dragging = False
            self.offset_x = 0
            self.offset_y = 0

        def update(self, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.is_dragging = True
                        self.offset_x = self.rect.x - event.pos[0]
                        self.offset_y = self.rect.y - event.pos[1]

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.is_dragging = False

            if self.is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y


    class puzzle_piece_two(pygame.sprite.Sprite):
        def __init__(self, image_path, width, height, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))

            self.is_dragging = False
            self.offset_x = 0
            self.offset_y = 0

        def update(self, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.is_dragging = True
                        self.offset_x = self.rect.x - event.pos[0]
                        self.offset_y = self.rect.y - event.pos[1]

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.is_dragging = False

            if self.is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y


    class puzzle_piece_three(pygame.sprite.Sprite):
        def __init__(self, image_path, width, height, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))

            self.is_dragging = False
            self.offset_x = 0
            self.offset_y = 0

        def update(self, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.is_dragging = True
                        self.offset_x = self.rect.x - event.pos[0]
                        self.offset_y = self.rect.y - event.pos[1]

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.is_dragging = False

            if self.is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    class puzzle_piece_four(pygame.sprite.Sprite):
        def __init__(self, image_path, width, height, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))

            self.is_dragging = False
            self.offset_x = 0
            self.offset_y = 0

        def update(self, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.is_dragging = True
                        self.offset_x = self.rect.x - event.pos[0]
                        self.offset_y = self.rect.y - event.pos[1]

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.is_dragging = False

            if self.is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
            

    while not level_complete:
        puzzle_width = int(WIDTH * 0.6)  
        puzzle_height = int(HEIGHT * 1.0)
        puzzle_x = 0
        puzzle_y = (HEIGHT - puzzle_height) // 2
        puzzle = puzzle(os.path.join("materials", "puzzle", "puzzle.png"), puzzle_width, puzzle_height, puzzle_x, puzzle_y)

        ppo_width = int(puzzle_width * 0.35)
        ppo_height = int(puzzle_height * 0.35)
        ppo = puzzle_piece_one(os.path.join("materials", "puzzle", "puzzle piece(1).png"), ppo_width, ppo_height, puzzle.rect.right -40, puzzle.rect.top - 30)

        ppt_width = int(puzzle_width * 0.35)
        ppt_height = int(puzzle_height * 0.35)
        ppt = puzzle_piece_two(os.path.join("materials", "puzzle", "puzzle piece(2).png"), ppt_width, ppt_height, ppo.rect.x , ppo.rect.y + offset_y)

        ppth_width = int(puzzle_width * 0.30)
        ppth_height = int(puzzle_height * 0.30)
        ppth = puzzle_piece_three(os.path.join("materials", "puzzle", "puzzle piece(3).png"), ppth_width, ppth_height, ppt.rect.x , ppt.rect.y + offset_y)

        ppf_width = int(puzzle_width * 0.35)
        ppf_height = int(puzzle_height * 0.35)
        ppf= puzzle_piece_four(os.path.join("materials", "puzzle", "puzzle piece(4).png"), ppf_width, ppf_height, ppth.rect.x , ppth.rect.y + offset_y)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(puzzle)
        all_sprites.add(ppo)
        all_sprites.add(ppt)
        all_sprites.add(ppth)
        all_sprites.add(ppf)

        right_section_width = screen_width // 3
        button_area_start_x = screen_width - right_section_width

        # Picture loading
        images = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        enter_img = pygame.image.load("materials/button/enter.png")
        enter_img = pygame.transform.scale(enter_img, (45, 45))

        for letter in letters:
            img = pygame.image.load(f"materials/button/letter_{letter}.png")
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
        correct_passcode = ['i', 'c', 'e']

        font = pygame.font.SysFont(None, 40)

        # Tutorial image
        steps = pygame.image.load("assets/Menu_interface/steps.png")
        steps = pygame.transform.scale(steps, (250, 350))
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        tutorial_duration = 4000
        tutorial_active = True
        tutorial_active_2 = False

        tutorial_start_time = pygame.time.get_ticks()
        tutorial_2_start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()

        text = "Click And Drag all the puzzle!!"
        text2 = "After that click the button on the right side"
        running = True
        while running:
            clock.tick(60)

            # ========== Event Handling ==========
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # letter buttons
                    clicked_btn = next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"),None)
                    if clicked_btn:
                        passcode.append(clicked_btn.letter)
                        clicked_btn.hide()

                    # ENTER
                    enter_clicked = next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"),None)
                    if enter_clicked:
                        if passcode == correct_passcode:
                            for btn in buttons:
                                btn.visible = False
                            congratulations = pygame.font.SysFont(None, 70).render("Congratulations!", True, (0, 148, 0))
                            screen.blit(congratulations,(400,305))
                            pygame.display.flip()
                            level_completed = True
                            time.sleep(1)
                            return "complete"
                        else:
                            print("❌ Invalid password")
                            passcode.clear()
                            for btn in buttons:
                                if btn.letter != "ENTER":
                                    btn.visible = True
                                        
            all_sprites.update(events)

            current_time = pygame.time.get_ticks()
            if tutorial_active and current_time - tutorial_start_time > tutorial_duration:
                tutorial_active = False
                tutorial_active_2 = True
                current_time += 1000
                tutorial_2_start_time = current_time

            if tutorial_active_2 and current_time - tutorial_2_start_time > tutorial_duration:
                tutorial_active_2 = False

            screen.blit(background_img, (0, 0))
            all_sprites.draw(screen)

            for btn in buttons:
                btn.draw()

            if tutorial_active:
                screen.blit(overlay, (0, 0))
                text_surface = font.render("Tutorial Level", True, (255, 255, 255))
                text_surface2 = font.render("Click and Drag the puzzle to the blank space !", True, (255, 255, 255))
                rect = text_surface.get_rect(center=(screen.get_width()//2, 250))
                rect2 = text_surface2.get_rect(center=(screen.get_width()//2, 300))
                screen.blit(text_surface, rect)
                screen.blit(text_surface2, rect2)
                pygame.display.flip()

            elif tutorial_active_2:
                screen.blit(overlay, (-480, 0))
                screen.blit(steps, (918,190))
                text_surface = font.render(text, True, (255, 255, 255))
                text_surface2 = font.render(text2, True, (255, 255, 255))
                rect = text_surface.get_rect(center=(screen.get_width()//4, 250))
                rect2 = text_surface2.get_rect(center=(screen.get_width()//4 + 50, 300))
                screen.blit(text_surface, rect)
                screen.blit(text_surface2, rect2)
                time.sleep(1)
                pygame.display.flip()

            pygame.display.flip()