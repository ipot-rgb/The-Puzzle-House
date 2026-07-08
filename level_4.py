def run_level_4(screen, hint_manager, preserve_state=False):
    import pygame
    import time
    import os
    import settings
    from hints_system import show_hint_popup
    level_complete = False

    # timer management (for refresh)
    if not hasattr(run_level_4, 'base_start_time'):
        run_level_4.base_start_time = None
        run_level_4.paused_time = 0
        run_level_4.timer_paused = False
        run_level_4.pause_start = 0

    if preserve_state and run_level_4.base_start_time is not None:
        start_timer = run_level_4.base_start_time
        paused_time = run_level_4.paused_time
        timer_paused = run_level_4.timer_paused
        pause_start = run_level_4.pause_start
    else:
        start_timer = pygame.time.get_ticks()
        run_level_4.base_start_time = start_timer
        paused_time = 0
        run_level_4.paused_time = 0
        timer_paused = False
        run_level_4.timer_paused = False
        pause_start = 0
        run_level_4.pause_start = 0

    #music management (for refresh)
    if not preserve_state:
        pygame.mixer.music.stop()
        
        if settings.music_on:
            pygame.mixer.music.load(os.path.join("materials", "bgm", "lv4.mp3"))
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
        pygame.display.set_caption("The Puzzle House - Level 4")

        # Cursors
        default_cursor = pygame.SYSTEM_CURSOR_ARROW
        hand_cursor = pygame.SYSTEM_CURSOR_HAND

        # ========== Button Configuration ==========
        background = pygame.image.load("assets/Level_12/wall.png")
        background = pygame.transform.scale(background, (screen_width, screen_height))

        enter_img = pygame.image.load("assets/Button_alphabet/enter.png")

        images = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        enter_img = pygame.transform.scale(enter_img, (45, 45))

        for letter in letters:
            img = pygame.image.load(f"assets/Button_alphabet/letter_{letter}.png")
            images[letter] = pygame.transform.scale(img, (45, 45))

        right_section_width = screen_width // 3
        button_start_x = screen_width - right_section_width

        button_size = 45
        button_gap = 80
        rows = 3

        cal_grid = lambda row: row * button_gap
        grid_width = cal_grid(rows)
        grid_height = cal_grid(rows)

        grid_x = button_start_x + (right_section_width - grid_width) // 2
        grid_y = (screen_height - grid_height) // 2

        buttons = []
        for i, letter in enumerate(letters):
            row = i // rows
            col = i % rows
            x = grid_x + col * button_gap
            y = grid_y + row * button_gap
            btn = Letter_Button(x, y, images[letter])
            btn.letter = letter
            buttons.append(btn)

        enter_x = grid_x + (grid_width // 2) - 22
        enter_y = grid_y + grid_height + 30
        enter_btn = Letter_Button(enter_x, enter_y, enter_img)
        enter_btn.letter = "ENTER"
        buttons.append(enter_btn)

        ui_font = pygame.font.Font(None, 36)
        hint_img = pygame.image.load("assets/Icon/hint_button.png")
        hint_img = pygame.transform.scale(hint_img, (60, 65))
        hint_button_rect = hint_img.get_rect(topleft=(1100, 20))

        refresh_img = pygame.image.load("assets/Icon/refresh_button.png").convert_alpha()
        refresh_img = pygame.transform.scale(refresh_img, (60, 65))
        refresh_button_rect = refresh_img.get_rect(topleft=(1030, 25))

        passcode = []
        correct_passcode = ['g','h','a','d']
        puzzles = []

        for btn in buttons:
            btn.draw()

        for i in range(1, 4):
            img = pygame.image.load(f"assets/Level_12/cat_0{i}.png")
            if i == 3:
                img = pygame.transform.scale(img, (100, 200))
                rect = img.get_rect(topleft=(200, 50))
            elif i == 2:
                img = pygame.transform.scale(img, (200, 500))
                rect = img.get_rect(topleft=(50, 100))
            else:
                img = pygame.transform.scale(img, (155, 455))
                rect = img.get_rect(topleft=(400, 80))

            puzzles.append({"img": img, "rect": rect, "original_rect": rect.copy()})

        active_puzzle = None

        setting_icon = pygame.image.load("assets/Icon/setting_button.png")
        setting_icon = pygame.transform.scale(setting_icon, (55, 55))
        setting_button = Button(45, 45, setting_icon)
        setting_button.update(screen)

        on_icon = pygame.image.load("assets/Icon/on_button.png")
        on_icon = pygame.transform.scale(on_icon, (75, 55))
        on_button = Button(700, 315, on_icon)

        off_icon = pygame.image.load("assets/Icon/off_button.png")  
        off_icon = pygame.transform.scale(off_icon, (75, 55))
        off_button = Button(700, 315, off_icon)

        close_icon = pygame.image.load("assets/Icon/close_icon.png")
        close_icon = pygame.transform.scale(close_icon, (23, 23))
        close_button = Button(820, 170, close_icon)

        font = pygame.font.Font('Notable-Regular.ttf', 60)
        
        settings_open = False
        run = True

        #timer pause tracking
        timer_paused = False
        timer_pause_start = 0

        while run:
            mouse_pos = pygame.mouse.get_pos()

            if settings_open and not timer_paused:
                timer_paused = True
                timer_pause_start = pygame.time.get_ticks()
                run_level_4.timer_paused = True
                run_level_4.pause_start = timer_pause_start
            elif not settings_open and timer_paused:
                timer_paused = False
                paused_time += pygame.time.get_ticks() - timer_pause_start
                run_level_4.paused_time = paused_time
                run_level_4.timer_paused = False
            
            # Handle cursor changes
            if settings_open:
                if close_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)
                elif settings.music_on and on_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)
                elif (not settings.music_on) and off_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)
                else:
                    pygame.mouse.set_cursor(default_cursor)
            else:
                if setting_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)
                else:
                    pygame.mouse.set_cursor(default_cursor)

            # ========== Event Handling ==========
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_pos = event.pos
                    
                    # ===== 1. Settings Button =====
                    if setting_button.is_clicked(click_pos):
                        settings_se = pygame.mixer.Sound("assets/sound_effect/setting_se.wav")
                        settings_se.play()
                        settings_open = not settings_open
                        continue
                    
                    # ===== 2. Settings Menu =====
                    if settings_open:
                        if close_button.is_clicked(click_pos):
                            settings_open = False
                            continue
                        elif settings.music_on and on_button.is_clicked(click_pos):
                            settings.music_on = False
                            pygame.mixer.music.set_volume(0)
                            print("music is off")
                            continue
                        elif (not settings.music_on) and off_button.is_clicked(click_pos):
                            settings.music_on = True
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.load(os.path.join("materials", "bgm", "lv4.mp3"))
                                pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(settings.music_volume)
                            print("music is on")
                            continue
                        continue
                    
                    # ===== 3. If settings is not open, handle game buttons =====
                    # Hint button
                    if hint_button_rect.collidepoint(click_pos):
                        ding = pygame.mixer.Sound("assets/sound_effect/ding_se.wav")
                        ding.play()
                        show_hint_popup(screen, hint_manager, 4, ui_font)
                        continue
                    
                    # Refresh button
                    if refresh_button_rect.collidepoint(click_pos):
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
                    
                    # Letter buttons (A-I)
                    clicked_btn = next(
                        (btn for btn in buttons 
                         if btn.rect.collidepoint(click_pos) 
                         and btn.visible 
                         and btn.letter != "ENTER"), 
                        None
                    )
                    if clicked_btn:
                        pop = pygame.mixer.Sound("assets/sound_effect/pop_se.wav")
                        pop.play()
                        passcode.append(clicked_btn.letter)
                        print(f"Clicked: {clicked_btn.letter}, passcode: {passcode}")
                        clicked_btn.hide()
                        continue
                    
                    # ENTER button
                    enter_clicked = next(
                        (btn for btn in buttons 
                         if btn.rect.collidepoint(click_pos) 
                         and btn.letter == "ENTER"), 
                        None
                    )
                    if enter_clicked:
                        if passcode == correct_passcode:
                            print("✅ You passed!")
                            total_elapsed = pygame.time.get_ticks() - start_timer - paused_time
                            timer_sec = total_elapsed / 1000
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
                            print("Game reset. Try again.")
                        continue
                    
                    # ===== 4. Puzzle Dragging =====
                    for i, p in enumerate(puzzles):
                        if p["rect"].collidepoint(click_pos):
                            active_puzzle = i
                            break

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # ✅ Only release puzzle if settings is closed
                    if not settings_open:
                        active_puzzle = None

                elif event.type == pygame.MOUSEMOTION:
                    # ✅ Only allow dragging if settings is closed and a puzzle is active
                    if not settings_open and active_puzzle is not None:
                        puzzles[active_puzzle]["rect"].move_ip(event.rel)
                        rect = puzzles[active_puzzle]["rect"]
                        rect.x = max(0, min(rect.x, screen_width - rect.width))
                        rect.y = max(0, min(rect.y, screen_height - rect.height))

            # ========== Drawing ==========
            screen.blit(background, (0, 0))
            
            for p in puzzles:
                screen.blit(p["img"], p["rect"])
            
            for btn in buttons:
                btn.draw()

            # Draw setting button (always on top)
            setting_button.update(screen)

            # Draw settings menu (if open)
            if settings_open:
                overlay = pygame.Surface(screen.get_size())
                overlay.fill((0, 0, 0))
                overlay.set_alpha(235)
                screen.blit(overlay, (0, 0))
                
                menu_rect = pygame.Rect(350, 150, 500, 300)
                pygame.draw.rect(screen, (40, 40, 40), menu_rect)
                pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)
                
                settings_text = font.render("SETTINGS", True, (255, 255, 255))
                screen.blit(settings_text, (420, 180))
                
                if settings.music_on:
                    on_button.update(screen)
                else:
                    off_button.update(screen)
                
                music_text = pygame.font.Font('Notable-Regular.ttf', 30)
                text = music_text.render("Music", True, (255, 255, 255))
                screen.blit(text, (450, 300))

                close_button.update(screen)
                
                if timer_paused:
                    total_elapsed = timer_pause_start - start_timer - paused_time
                else:
                    total_elapsed = pygame.time.get_ticks() - start_timer - paused_time
                timer_sec = total_elapsed / 1000
                # print(f"Current time: {timer_sec:.2f} seconds")

                # ===== Display Timer =====
                timer_font = pygame.font.Font('Orbitron-VariableFont_wght.ttf', 36)
                minutes = int(timer_sec // 60)
                seconds = int(timer_sec % 60)
                milliseconds = int((timer_sec % 1) * 100)
                timer_text = f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
                time_surface = timer_font.render(timer_text, True, (255, 255, 255))
                screen.blit(time_surface, (510, 390)) 

            # Hint and Refresh buttons
            screen.blit(hint_img, hint_button_rect)
            screen.blit(refresh_img, refresh_button_rect)

            pygame.display.flip()