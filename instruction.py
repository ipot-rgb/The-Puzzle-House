import pygame
import time

def show_instruction(screen, font):
    #lines showed in instruction page
    lines = [
        "Welcome to The Puzzle House!",
        "",
        "In each level, you must find the correct passcode.",
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