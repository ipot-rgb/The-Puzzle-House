import pygame


class LevelGame:

    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()


        self.running = True
        self.level_complete = False


    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quit entire game

            # Your custom event handling here
            if event.type == pygame.MOUSEBUTTONDOWN:
                # == Check LETTER button click ==
                if (clicked_btn := next((btn for btn in buttons if
                                         btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"),
                                        None)):
                    if True:
                        passcode.append(clicked_btn.letter)
                        print(f"Clicked: {clicked_btn.letter}, passcode: {passcode}")
                        clicked_btn.hide()

                # == Check ENTER button click ==
                # Checking if the click is on the ENTER button and if it's visible (not hidden)
                elif (enter_clicked := next(
                        (btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"), None)):
                    if True:
                        if passcode == correct_passcode:
                            print("✅ You passed!")

                        else:
                            print(f"❌ Invalid password: {passcode}")
                            # Reset buttons
                            for btn in buttons:
                                if btn.letter != "ENTER":
                                    btn.visible = True
                                    btn.clicked = False
                            passcode = []
                            print("Game reset. Try again.")

        return True  # Continue running
