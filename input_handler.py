import pygame
import time

class InputHandler:
    def __init__(self):
        self.bpm_adjust_amount = 10 

    def get_integer_input(self, current_text, event):
        """Gets user input, ensuring only positive integers are allowed.

        Args:
            current_text: The current text in the input box.
            event: The pygame event object.

        Returns:
            tuple: A tuple containing the updated text and a boolean indicating if Enter was pressed.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return current_text[:-1], False
            elif event.unicode.isdigit():
                return current_text + event.unicode, False
            elif event.key == pygame.K_RETURN:
                try:
                    if int(current_text) > 0:
                        return current_text, True  # Indicate Enter key press
                    else:
                        return current_text, False  # Invalid input
                except ValueError:
                    return current_text, False  # Invalid input
        return current_text, False

    def handle_bpm_adjustment(self, event):
        """Handles BPM adjustment with key presses.

        Args:
            event: The pygame event object.

        Returns:
            int: The amount to adjust the BPM.
        """
        bpm_adjustment = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bpm_adjustment = self.bpm_adjust_amount
            elif event.key == pygame.K_DOWN:
                bpm_adjustment = -self.bpm_adjust_amount

        return bpm_adjustment
