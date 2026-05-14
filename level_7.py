def run_level_7(screen,hint_manager):
    import pygame
    import time
    from hints_system import show_hint_popup
    level_complete = False
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

    def clamp_rect_to_bounds(rect, bounds):
        rect.x = max(bounds.x, min(rect.x, bounds.right - rect.width))
        rect.y = max(bounds.y, min(rect.y, bounds.bottom - rect.height))

    while not level_complete:
        #===============================
        # Screen Setup
        #===============================
        screen_width = 1200
        screen_height = 650
        pygame.display.set_caption("The Puzzle House")
        red = (207, 177, 177)

        # Cursors
        default_cursor = pygame.SYSTEM_CURSOR_ARROW
        hand_cursor = pygame.SYSTEM_CURSOR_HAND

        # ========== Button Configuration ==========
        board = pygame.image.load("assets/Level_15/board.png")

        # Paper images
        paper = pygame.image.load("assets/Level_15/paper.png")
        paper = pygame.transform.scale(paper, (400, 400))

        # Background image
        brg = pygame.image.load("assets/Level_15/brg_15.png")
        brg = pygame.transform.scale(brg, (screen_width, screen_height))

        # Tutorial image
        steps = pygame.image.load("assets/Menu_interface/steps.png")
        steps = pygame.transform.scale(steps, (250, 350))

        # A-I button setup
        images = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]


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
        enter_img = pygame.image.load("assets/Button_alphabet/enter.png")
        enter_img = pygame.transform.scale(enter_img, (45, 45))
        enter_x = grid_x + (grid_width // 2) - 22       # 680 + (240 // 2) - 22 = 798
        enter_y = grid_y + grid_height + 30             # 205 + 240 + 30 = 475
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
        correct_passcode = ['i', 'h', 'b', 'a', 'd', 'g', 'f', 'e', 'c']


        puzzles = []

        for i in range(1, 2):
            rect_paper = paper.get_rect(topleft=(450, 200))
            puzzles.append({"img": paper, "rect": rect_paper})

        for i in range(1, 10):
            img = pygame.image.load(f"assets/Level_15/num_{i}.png")
            if i == 2:
                img = pygame.transform.scale(img, (110, 150))
            elif i == 4:
                img = pygame.transform.scale(img, (80, 100))
            else:
                img = pygame.transform.scale(img, (100, 100))

            rect = img.get_rect(topleft=(80 * i, 56))
            puzzles.append({"img": img, "rect": rect})

        active_puzzle = None
        active_paper = None

        font = pygame.font.SysFont(None, 40)

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        tutorial_start_time = pygame.time.get_ticks()
        tutorial_duration = 3000   # 3秒（毫秒）
        tutorial_active = True
        tutorial_active_2 = True

        clock = pygame.time.Clock()

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
                        show_hint_popup(screen, hint_manager, 7, ui_font)
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
                            time.sleep(1)
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
                        active_paper = None

                elif event.type == pygame.MOUSEMOTION:
                        if active_puzzle is not None:
                            puzzles[active_puzzle]["rect"].move_ip(event.rel)
                            rect = puzzles[active_puzzle]["rect"]
                            rect.x = max(0, min(rect.x, screen_width - rect.width))
                            rect.y = max(0, min(rect.y, screen_height - rect.height))
                        elif active_paper is not None:
                            puzzles[active_paper]["rect_paper"].move_ip(event.rel)
                            paper_rect = puzzles[active_paper]["rect_paper"]
                            paper_rect.x = max(0, min(paper_rect.x, screen_width - paper_rect.width))
                            paper_rect.y = max(0, min(paper_rect.y, screen_height - paper_rect.height))
                            
            screen.blit(brg, (0, 0))
            screen.blit(board, (35, 200))
            pygame.draw.rect(screen, red, (830, 0, screen_width - 830, screen_height))
            for btn in buttons:
                btn.draw()

            for p in puzzles:
                screen.blit(p["img"], p["rect"])

            #draw the hint button
            screen.blit(hint_img, hint_button_rect)

            pygame.display.flip()
