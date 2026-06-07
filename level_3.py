def run_level_3(screen, hint_manager, preserve_state=False):
    import pygame
    import time
    import os
    from hints_system import show_hint_popup
    level_complete = False

    #timer management (for refresh)
    if not hasattr(run_level_3, 'base_start_time'):
        run_level_3.base_start_time = None

    if preserve_state and run_level_3.base_start_time is not None:
        start_timer = run_level_3.base_start_time
    else:
        start_timer = pygame.time.get_ticks()
        run_level_3.base_start_time = start_timer

    pygame.mixer.music.load(os.path.join("materials", "bgm", "lv3.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


    while not level_complete:
        class Button:
            def __init__(self, x, y, image):
                self.image = image
                self.x = x
                self.y = y
                self.rect = self.image.get_rect(center=(x, y))
                self.visible = True

            def update(self, display):
                if self.visible:
                    display.blit(self.image, self.rect)

            def is_clicked(self, pos):
                return self.rect.collidepoint(pos) and self.visible

            def is_hovered(self, pos):
                return self.rect.collidepoint(pos)

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

            def is_clicked(self, pos):
                return self.rect.collidepoint(pos)

            def is_hovered(self, pos):
                return self.rect.collidepoint(pos)

        #===============================
        # Screen Setup
        #===============================        
        screen_width = 1200
        screen_height = 650
        pygame.display.set_caption("The Puzzle House - Level 3")

        # Cursors
        default_cursor = pygame.SYSTEM_CURSOR_ARROW
        hand_cursor = pygame.SYSTEM_CURSOR_HAND

        # ========== Button Configuration ==========
        # Picture loading
        background = pygame.image.load("assets/Level_11/background.png")
        background = pygame.transform.scale(background, (screen_width, screen_height))

        enter_img = pygame.image.load("assets/Button_alphabet/enter.png")

        # A-I button setup
        images = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        enter_img = pygame.transform.scale(enter_img, (45, 45))

        for letter in letters:
            img = pygame.image.load(f"assets/Button_alphabet/letter_{letter}.png")
            images[letter] = pygame.transform.scale(img, (45, 45))

        # Right section dimensions


        right_section_width = screen_width // 3     # 800
        button_start_x = screen_width - right_section_width     # 400

        # Configure button grid
        button_size = 45
        button_gap = 80
        rows = 3

        cal_grid = lambda row: row * button_gap
        grid_width = cal_grid(rows)  # 240
        grid_height = cal_grid(rows) # 240

        # Letters grid start position (centered in the right section)
        grid_x = button_start_x + (right_section_width - grid_width) // 2  # 400 + (800- 240) //2 = 680
        grid_y = (screen_height - grid_height) // 2                        # (650 - 240) //2 = 205

        # Create letter buttons
        buttons = []
        for i, letter in enumerate(letters):
            row = i // rows
            col = i % rows      # 3x3
            x = grid_x + col * button_gap
            y = grid_y + row * button_gap
            btn = Letter_Button(x, y, images[letter])
            btn.letter = letter
            buttons.append(btn)

        # ENTER Button
        enter_x = grid_x + (grid_width // 2) - 22 # 680 + ()
        enter_y = grid_y + grid_height + 30
        enter_btn = Letter_Button(enter_x, enter_y, enter_img)
        enter_btn.letter = "ENTER"
        buttons.append(enter_btn)

        # Hint Button
        ui_font = pygame.font.Font(None, 36)
        hint_img = pygame.image.load("assets/Icon/hint_button.png")
        hint_img = pygame.transform.scale(hint_img, (60, 65))
        hint_button_rect = hint_img.get_rect(topleft=(1100, 20))

        #refresh button
        ui_font = pygame.font.Font(None, 36)
        refresh_img = pygame.image.load("assets/Icon/refresh_button.png").convert_alpha()
        refresh_img = pygame.transform.scale(refresh_img, (60, 65))
        refresh_button_rect = refresh_img.get_rect(topleft=(1030, 25))

        # Passcode variables
        passcode = []
        correct_passcode = ['c','f','i','h','e','b','a']
        puzzles = []

        # Button Drawing
        for btn in buttons:
            btn.draw()

        for i in range(1, 8):
            img = pygame.image.load(f"assets/Level_11/puzzle_0{i}.png")
            if i == 2:
                img = pygame.transform.scale(img, (180, 268))
                rect = img.get_rect(topleft=(180, 268))
            elif i == 1: 
                img = pygame.transform.scale(img, (162, 130))
                rect = img.get_rect(topleft=(162, 130))
            elif i == 4:
                img = pygame.transform.scale(img, (180,140))
                rect = img.get_rect(topleft=(180,140))
            elif i == 5:
                img = pygame.transform.scale(img, (165, 250))
                rect = img.get_rect(topleft=(165, 250))
            elif i == 6:
                img = pygame.transform.scale(img, (170, 252))
                rect = img.get_rect(topleft=(170, 252))
            else:
                img = pygame.transform.scale(img, (176, 136))
                rect = img.get_rect(topleft=(176, 136))
            puzzles.append({"img": img, "rect": rect, "original_rect": rect.copy()})


        active_puzzle = None

        run = True
        while run:
            mouse_pos = pygame.mouse.get_pos()
            pygame.mouse.set_cursor(default_cursor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # --- check hint button click ---
                    if hint_button_rect.collidepoint(event.pos):
                        ding = pygame.mixer.Sound("assets/sound_effect/ding_se.wav")
                        ding.play()
                        show_hint_popup(screen, hint_manager, 3, ui_font)
                    #refresh button click
                    if refresh_button_rect.collidepoint(event.pos):
                        click_se = pygame.mixer.Sound("assets/sound_effect/pop_se.wav")
                        click_se.play()
                        for puzzle in puzzles:
                            puzzle["rect"].x = puzzle["original_rect"].x
                            puzzle["rect"].y = puzzle["original_rect"].y
                        for btn in buttons:
                            if btn.letter != "ENTER":
                                btn.visible = True
                        passcode = []
                        return ("refresh",)
                    # Button Click Detection
                    if (clicked_btn := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"), None)):
                        pop = pygame.mixer.Sound("assets/sound_effect/pop_se.wav")
                        pop.play()
                        passcode.append(clicked_btn.letter)
                        clicked_btn.hide()

                    elif (enter_clicked := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"), None)):
                        if passcode == correct_passcode:
                            timer_sec = (pygame.time.get_ticks() - start_timer) / 1000
                            for btn in buttons:
                                btn.visible = False
                            pygame.display.flip()
                            level_completed = True
                            celebrate = pygame.mixer.Sound("assets/sound_effect/celebrate_se.wav")
                            celebrate.play()
                            time.sleep(1)
                            return "complete", timer_sec
                        else:
                            wrong = pygame.mixer.Sound("assets/sound_effect/wrong_se.wav")
                            wrong.play()
                            for btn in buttons:
                                if btn.letter != "ENTER":
                                    btn.visible = True
                            passcode = []

                    # Puzzle Dragging Detection
                    elif event.button == 1:
                        for i, p in enumerate(puzzles):
                            if p["rect"].collidepoint(event.pos):
                                active_puzzle = i
                    current_time = time.time()

                elif event.type == pygame.MOUSEBUTTONUP:
                        active_puzzle = None

                elif event.type == pygame.MOUSEMOTION:
                        if active_puzzle is not None:
                            puzzles[active_puzzle]["rect"].move_ip(event.rel)
                            rect = puzzles[active_puzzle]["rect"]
                            rect.x = max(0, min(rect.x, screen_width - rect.width))
                            rect.y = max(0, min(rect.y, screen_height - rect.height))
            screen.blit(background, (0,0))
            for btn in buttons:
                btn.draw()
            for p in puzzles:
                screen.blit(p["img"], p["rect"])

            #hint button
            screen.blit(hint_img, hint_button_rect)
            #refresh button
            screen.blit(refresh_img, refresh_button_rect)
            pygame.display.flip()
