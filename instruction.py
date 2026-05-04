import pygame
import time

def show_instruction(screen, font):
    #lines showed in instruction page
    lines = [
        "Welcome to The Puzzle House",
        "",
        "In each level, you must find the correct passcode.",
        "The number of character in each passcode ranges from 1-9",
        "Click on the letter buttons to enter your answer.",
        "Press 'ENTER' button to submit.",
        "",
        "This is a test for your creativity",
        "and also your intelligence",
        "Finish the levels to prove your worth!!"
        "",
        "Good luck!",
    ]

    # Configuration
    char_delay = 0.05  # seconds per character
    line_pause = 0.5  # seconds after each full line
    final_pause = 1.0  # seconds after all lines before white flash
    flash_duration = 0.5

    screen_width, screen_height = screen.get_size()
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)

    #backgound colours
    background = pygame.Surface((screen_width, screen_height))
    background.fill(bg_color)

    clock = pygame.time.Clock()

    #typewriter state
    full_text = "\n".join(lines)
    displayed_text = ""
    last_char_time = time.time()
    current_line_index = 0
    lines_rendered = lines.copy()

    skip = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                skip = True
                break
        if skip:
            break

        #typewriter effect: add characters over time
        if len(displayed_text) < len(full_text):
            if time.time() - last_char_time >= char_delay:
                displayed_text += full_text[len(displayed_text)]
                last_char_time = time.time()
        else:
            time.sleep(final_pause)
            running = False
            break

        screen.blit(background, (0, 0))

        #split displayed text into lines (to handle wrapping)
        #split by newline and render each line
        display_lines = displayed_text.split("\n")
        y_offset = 100
        line_spacing = font.get_height() + 10
        for i, line in enumerate(display_lines):
            if line.strip() == "":
                y_offset += line_spacing
                continue
            text_surf = font.render(line, True, text_color)
            #center the text horizontally
            x = (screen_width - text_surf.get_width()) // 2
            screen.blit(text_surf, (x, y_offset))
            y_offset += line_spacing

        pygame.display.flip()
        clock.tick(60)

    # ---- White flash effect ----
    flash_start = time.time()
    flash_surf = pygame.Surface((screen_width, screen_height))
    flash_surf.fill((255, 255, 255))
    while time.time() - flash_start < flash_duration:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        alpha = int(255 * (1 - (time.time() - flash_start) / flash_duration))
        flash_surf.set_alpha(alpha)
        screen.blit(flash_surf, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    #final short pause
    time.sleep(0.2)