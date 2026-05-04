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

        #placeholder for other levels that does not have hints
        for level in range(1, 10):
            if level not in self._hints_db:
                self._hints_db[level] = [
                    f"Level {level} – First hint (customize in hint_system.py)",
                    f"Level {level} – Second hint",
                    f"Level {level} – Third hint"
                ]

        #track how many hints have been used per level
        self._used = {level: 0 for level in range(1, 10)}

    def get_next_hint(self, level):
        #return (hint_text, remaining_hints). If no hints left, return (message, 0)."""
        used = self._used.get(level, 0)
        if used >= 3:
            return ("No more hints available for this level.", 0)
        hint_text = self._hints_db[level][used]
        self._used[level] = used + 1
        remaining = 3 - (used + 1)
        return (hint_text, remaining)

