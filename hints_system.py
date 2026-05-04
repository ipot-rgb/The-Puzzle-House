import pygame

class HintManager:
    def __init__(self):
        self._hints_db = {
            1: [
                "Hint 1 for Level 1: The passcode contains 5 characters.",
                "Hint 2 for Level 1: Try dragging the bookmark and see which line where the letters fit the dots",
                "Hint 3 for Level 1: The answer is 'c','d','h','b','a'"
            ],
            7: [
                "Hint 1 for Level 7: This level has 9 letters.",
                "Hint 2 for Level 7: Try arranging these numbers alphabetically.",
                "Hint 3 for Level 7: Follow the 9 pattern grid to find the correct order."
            ],
            8: [
                "Hint 1 for Level 8: Placeholder_1",
                "Hint 2 for Level 8: Placeholder_2",
                "Hint 3 for Level 8: Placeholder_3"
            ]
        }