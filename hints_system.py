import pygame

class HintManager:
    def __init__(self):
        self._hints_db = {
            1: [
                "Hint 1 for Level 1: The passcode contains 5 characters",
                "Hint 2 for Level 1: Try dragging the bookmark and see which line where the letters fit the dots",
                "Hint 3 for Level 1: The answer is 'C','D','H','B','A'"
            ],
            
            2: [
                "Hint 1 for Level 2: Hold and drag your mouse cursor",
                "Hint 2 for Level 2: The passcode contains 4 characters",
                "Hint 3 for Level 2: The answer is 'B' 'C' 'F' 'I' ",
            ],

            3: [
                "Hint 1 for level 3: This level solution is a guide line",
                "Hint 2 for level 3: All the puzzle will not overlay to each other",
                "Hint 3 for level 3: The answer is 'C' 'F' 'I' 'H' 'E' 'B' 'A'",
            ],

            5: [ 
                "Hint 1 for level 5: This level have 4 charecters",
                "Hint 2 for level 5: There are two cats are looking each other",
                "Hint 3 for level 5: The smallest cat should be on the bottom of them",
            ],

            7: [
                "Hint 1 for Level 7: Follow the 9 pattern grid to find the correct order",
                "Hint 2 for Level 7: The paper is the last steps for reviewing the answer",
                "Hint 3 for Level 7: The final passcode is 'I' 'H' 'B' 'A' 'D' 'G' 'F' 'E' 'C' "
            ],

            8: [
                "Hint 1 for Level 8: This level include 4 characters",
                "Hint 2 for Level 8: The fish head and tail is apart of puzzle",
                "Hint 3 for Level 8: The answer is 'A' 'I' 'G' 'B'"
            ]
        }

        #placeholder for other levels that does not have hints
        for level in range(1, 10):
            if level not in self._hints_db:
                self._hints_db[level] = [
                    f"Level {level}: First hint (customize in hint_system.py)",
                    f"Level {level}: Second hint",
                    f"Level {level}: Third hint"
                ]

        #track how many hints have been used per level
        self._used = {level: 0 for level in range(1, 10)}

    def get_next_hint(self, level):
        #return (hint_text, remaining_hints). If no hints left, return (message, 0)
        used = self._used.get(level, 0)
        if used >= 3:
            return ("No more hints available for this level.", 0)
        hint_text = self._hints_db[level][used]
        self._used[level] = used + 1
        remaining = 3 - (used + 1)
        return (hint_text, remaining)

def show_hint_popup(screen, hint_manager, level, font):
    background = screen.copy()
    popup_width, popup_height = 500, 300
    popup_rect = pygame.Rect(
        screen.get_width() // 2 - popup_width // 2,
        screen.get_height() // 2 - popup_height // 2,
        popup_width, popup_height
    )

    #buttons
    get_hint_rect = pygame.Rect(popup_rect.x + 50, popup_rect.y + popup_height - 60, 180, 40)
    close_rect = pygame.Rect(popup_rect.x + popup_width - 230, popup_rect.y + popup_height - 60, 180, 40)

    colors = {
        "bg": (50, 50, 70),
        "border": (200, 200, 200),
        "button": (100, 150, 200),
        "button_hover": (150, 200, 250),
        "text": (255, 255, 255)
    }
    used = hint_manager._used.get(level, 0)
    remaining = 3 - used
    hint_text = ""
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if close_rect.collidepoint(pos):
                    running = False
                    return
                if get_hint_rect.collidepoint(pos):
                    hint_text, remaining = hint_manager.get_next_hint(level)

        #mouse
        mouse_pos = pygame.mouse.get_pos()
        get_hover = get_hint_rect.collidepoint(mouse_pos)
        close_hover = close_rect.collidepoint(mouse_pos)

        # Overlay and popup
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, colors["bg"], popup_rect, border_radius=10)
        pygame.draw.rect(screen, colors["border"], popup_rect, 3, border_radius=10)

        #draw hint text
        if hint_text:
            words = hint_text.split(' ')
            lines = []
            current_line = []
            for w in words:
                test_line = ' '.join(current_line + [w])
                test_surf = font.render(test_line, True, colors["text"])
                if test_surf.get_width() < popup_width - 40:
                    current_line.append(w)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [w]
            if current_line:
                lines.append(' '.join(current_line))

            y = popup_rect.y + 30
            for line in lines:
                surf = font.render(line, True, colors["text"])
                screen.blit(surf, (popup_rect.x + 20, y))
                y += font.get_height() + 5
        else:
            msg = font.render("Press 'Get New Hint' to receive a hint.", True, colors["text"])
            screen.blit(msg, (popup_rect.x + 20, popup_rect.y + 30))

        #show remaining hints
        rem_surf = font.render(f"Hints left: {remaining}", True, (200, 200, 100))
        screen.blit(rem_surf, (popup_rect.x + 20, popup_rect.y + popup_height - 100))

        #draw buttons
        pygame.draw.rect(screen, colors["button_hover"] if get_hover else colors["button"], get_hint_rect, border_radius=5)
        pygame.draw.rect(screen, colors["button_hover"] if close_hover else colors["button"], close_rect, border_radius=5)
        get_text = font.render("Get New Hint", True, (0, 0, 0))
        close_text = font.render("Close", True, (0, 0, 0))
        screen.blit(get_text, (get_hint_rect.x + 30, get_hint_rect.y + 10))
        screen.blit(close_text, (close_rect.x + 60, close_rect.y + 10))

        pygame.display.flip()
        clock.tick(60)


