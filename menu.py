import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36) 

        # Define button rectangles (adjust positions as needed)
        self.play_button_rect = pygame.Rect(300, 200, 200, 50)
        self.record_button_rect = pygame.Rect(300, 300, 200, 50)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                selected_option = self.handle_event(event)  # Call handle_event() to get selected option
                if selected_option == "record":
                    return "record"
                elif selected_option == "play":
                    return "play"

            self.screen.fill((255, 255, 255)) 
            self.draw_menu()
            pygame.display.flip()

        return "menu"  # Return "menu" if the loop exits without a selection

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button_rect.collidepoint(mouse_pos):
                return "play"
            elif self.record_button_rect.collidepoint(mouse_pos):
                return "record"
        return "menu"

    def draw_menu(self):
        text_color = (0, 0, 0)
        
        # Draw "Play Game" button
        pygame.draw.rect(self.screen, (200, 200, 200), self.play_button_rect) 
        play_text = self.font.render("Play Game", True, text_color)
        play_text_rect = play_text.get_rect(center=self.play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)

        # Draw "Record Ostinato" button
        pygame.draw.rect(self.screen, (200, 200, 200), self.record_button_rect)
        record_text = self.font.render("Record Ostinato", True, text_color)
        record_text_rect = record_text.get_rect(center=self.record_button_rect.center)
        self.screen.blit(record_text, record_text_rect)
