def run_level_1(screen):
    level_complete = False
    while not level_complete:
        import pygame
        import os

        screen_width = 1200
        screen_height = 650
        # background
        background_img = pygame.image.load(os.path.join("materials", "lv1 background.png")).convert()
        background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

        # sprite class for the note
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

        pygame.display.set_caption("The Puzzle House")

        # Cursors
        default_cursor = pygame.SYSTEM_CURSOR_ARROW
        hand_cursor = pygame.SYSTEM_CURSOR_HAND

        # ========== Button Configuration ==========
        enter_img = pygame.image.load("assets/Button_alphabet/enter.png")

        # A-I button setup
        images = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        enter_img = pygame.transform.scale(enter_img, (45, 45))

        for letter in letters:
            img = pygame.image.load(f"assets/Button_alphabet/letter_{letter}.png")
            images[letter] = pygame.transform.scale(img, (45, 45))

        # Right section dimension
        right_section_width = screen_width // 3  # 800
        button_start_x = screen_width - right_section_width  # 400

        # Configure button grid
        button_size = 45
        button_gap = 80
        rows = 3

        grid_width = rows * button_gap  # 240
        grid_height = rows * button_gap  # 240

        # Letters grid start position (centered in the right section)
        grid_x = button_start_x + (right_section_width - grid_width) // 2  # 400 + (800- 240) //2 = 680
        grid_y = (screen_height - grid_height) // 2  # (650 - 240) //2 = 205

        # Create letter buttons
        buttons = []
        for i, letter in enumerate(letters):
            row = i // rows
            col = i % rows  # 3x3
            x = grid_x + col * button_gap
            y = grid_y + row * button_gap
            btn = Letter_Button(x, y, images[letter])
            btn.letter = letter
            buttons.append(btn)

        # ENTER Button
        enter_x = grid_x + (grid_width // 2) - 22  # 680 + ()
        enter_y = grid_y + grid_height + 30
        enter_btn = Letter_Button(enter_x, enter_y, enter_img)
        enter_btn.letter = "ENTER"
        buttons.append(enter_btn)

        # Passcode variables
        passcode = []
        correct_passcode = ['c','d','h','b','a']

        # Button Drawing
        for btn in buttons:
            btn.draw()

        class Note(pygame.sprite.Sprite):
            def __init__(self, image_path, width, height, x, y):
                super().__init__()
                self.image = pygame.image.load(image_path).convert()
                self.image = pygame.transform.scale(self.image, (width, height))
                self.rect = self.image.get_rect()
                self.rect.topleft = (x, y)



        class Bookmark(pygame.sprite.Sprite):
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


        note_width = int(screen_width * 0.65)
        note_height = int(screen_height * 0.9)
        note_x = 0
        note_y = (screen_height - note_height) // 2
        note = Note(os.path.join("materials", "lv1 note.png"), note_width, note_height, note_x, note_y)

        bm_width = int(note_width * 0.9)
        bm_height = int(note_height * 1.0)
        bm = Bookmark(os.path.join("materials", "book mark.png"),
                      bm_width, bm_height,
                      note_x + int(note_width * 0.6), note_y + 50)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(note)
        all_sprites.add(bm)

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # == Check LETTER button click ==
                    if (clicked_btn := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"),None)):
                        if True:
                            passcode.append(clicked_btn.letter)
                            print(f"Clicked: {clicked_btn.letter}, passcode: {passcode}")
                            clicked_btn.hide()

                    # == Check ENTER button click ==
                    # Checking if the click is on the ENTER button and if it's visible (not hidden)
                    elif (enter_clicked := next((btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"),None)):
                        if True:
                            if passcode == correct_passcode:
                                print("✅ You passed!")
                                congratulations = pygame.font.SysFont(None, 70).render("Congratulations!", True,(0, 128, 0))
                                screen.blit(congratulations, (400, 305))
                                pygame.display.flip()
                                level_completed = True
                                return "complete"
                            else:
                                print(f"❌ Invalid password: {passcode}")
                                # Reset buttons
                                for btn in buttons:
                                    if btn.letter != "ENTER":
                                        btn.visible = True
                                        btn.clicked = False
                                passcode = []
                                print("Game reset. Try again.")


            # Button drawing
            for btn in buttons:
                btn.draw()

            # Disappearing buttons
            for btn in buttons:
                if not btn.visible and btn.letter != "ENTER":
                    font = pygame.font.Font(None, 36)
                    check = font.render("", True, (0, 255, 0))
                    screen.blit(check, (btn.rect.centerx - 15, btn.rect.centery - 15))

            bm.update(events)

            screen.blit(background_img, (0, 0))
            all_sprites.draw(screen)
            for btn in buttons:
                btn.draw()
            font = pygame.font.Font(None, 36)
            pygame.display.update()

        pygame.quit()
