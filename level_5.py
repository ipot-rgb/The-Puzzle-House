def run_level_5(screen, hint_manager):
    import pygame
    import time
    from hints_system import show_hint_popup
    level_complete = False
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
        pygame.display.set_caption("The Puzzle House")

        # Cursors
        default_cursor = pygame.SYSTEM_CURSOR_ARROW
        hand_cursor = pygame.SYSTEM_CURSOR_HAND

        # ========== Button Configuration ==========
        # Picture loading
        background = pygame.image.load("assets/Level_12/wall.png")
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

        # Passcode variables
        passcode = []
        correct_passcode = ['g','h','a','d']
        puzzles = []

        # Button Drawing
        for btn in buttons:
            btn.draw()

        for i in range(1, 4):
            img = pygame.image.load(f"assets/Level_12/cat_0{i}.png")
            if i == 3:
                img = pygame.transform.scale(img, (200, 400))
                rect = img.get_rect(topleft=(200, 50))   # Changed Y to 50
            elif i == 2:
                img = pygame.transform.scale(img, (250, 550))
                rect = img.get_rect(topleft=(50, 100))   # Changed position
            else:
                img = pygame.transform.scale(img, (205, 505))
                rect = img.get_rect(topleft=(400, 80))   # Changed position

            puzzles.append({"img": img, "rect": rect})

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
                        show_hint_popup(screen, hint_manager, 5, ui_font)
                    # Button Click Detection
                    if (clicked_btn := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"), None)):
                        passcode.append(clicked_btn.letter)
                        clicked_btn.hide()

                    elif (enter_clicked := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"), None)):
                        if passcode == correct_passcode:
                            for btn in buttons:
                                btn.visible = False
                            congratulations = pygame.font.SysFont(None, 70).render("Congratulations!", True, (0, 128, 0))
                            screen.blit(congratulations,(400,305))
                            pygame.display.flip()
                            level_completed = True
                            time.sleep(3)
                            return "complete"
                        else:
                            print("❌ Incorrect passcode, try again.")
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
            screen.blit(background, (0,0))
            for btn in buttons:
                btn.draw()
            for p in puzzles:
                screen.blit(p["img"], p["rect"])

            # draw the hint button
            screen.blit(hint_img, hint_button_rect)
            pygame.display.flip()
