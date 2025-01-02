import pygame
import time

class InputHandler:
    def __init__(self):
        self.last_key_press_time = 0 
        self.key_repeat_delay = 500  # Initial delay in milliseconds 
        self.min_repeat_delay = 50   # Minimum delay between adjustments
        self.bpm_adjust_amount = 1  # Amount to adjust BPM per key press
        self.bpm_adjust_direction = 0  # 1 for up, -1 for down, 0 for none

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

    def handle_bpm_adjustment(self, current_bpm, event, dt):
        """Handles BPM adjustment with key presses and smoother speed control.

        Args:
            current_bpm: The current BPM value.
            event: The pygame event object.
            dt: Time delta since the last frame.

        Returns:
            tuple: A tuple containing the updated BPM value and a boolean indicating if BPM was adjusted.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("Key UP pressed")
                self.bpm_adjust_direction = 1 
                self.last_key_press_time = pygame.time.get_ticks() 

            elif event.key == pygame.K_DOWN:
                print("Key DOWN pressed")
                self.bpm_adjust_direction = -1
                self.last_key_press_time = pygame.time.get_ticks() 

        if event.type == pygame.KEYUP and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
            print("Key released")
            self.bpm_adjust_direction = 0  # Stop adjusting when key is released

        current_time = pygame.time.get_ticks()

        if self.bpm_adjust_direction != 0: 
            if current_time - self.last_key_press_time > self.key_repeat_delay:
                new_bpm = current_bpm + (self.bpm_adjust_direction * self.bpm_adjust_amount)
                new_bpm = max(10, min(new_bpm, 999))  # Limit BPM range 
                self.last_key_press_time = current_time 
                # Gradually decrease the delay (up to a minimum)
                self.key_repeat_delay = max(self.min_repeat_delay, self.key_repeat_delay - 5) 
                print(f"Adjusting BPM. Current BPM: {current_bpm}")
                print(f"New BPM: {new_bpm}")
                return new_bpm, True 

        return current_bpm, False 
