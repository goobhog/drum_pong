import pygame
import math
import time
import mido
from pygame.locals import *
from ball import Ball  # Assuming you have a 'ball.py' file with the Ball class

# Initialize Pygame
pygame.init()

# Set the display size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rhythm Game")

# Ball properties
initial_y = screen_height * 2 // 3  # Start at the bottom third
min_radius = 5
max_radius = 50
ball_color = (0, 0, 255)  # Blue
bpm = 120  # Initial BPM
beats_per_measure = 4
measures_per_sequence = 4  # Number of measures per sequence
sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence  # Calculate sequence duration in seconds

# Timing variables
start_time = time.time()
cycle_start_time = time.time()  # Store the start time of the current sequence
cycle_count = 0
current_measure = 1

# Pattern recording variables
recording = False
pattern = []

# Initialize MIDI input
try:
    midi_in = mido.open_input()
except:
    print("No MIDI input devices found.")
    midi_in = None

# Font for displaying BPM
font = pygame.font.Font(None, 36)

# Create text input boxes
bpm_input_box = pygame.Rect(10, 10, 140, 32)
bpm_color_inactive = pygame.Color('lightskyblue3')
bpm_color_active = pygame.Color('dodgerblue2')
bpm_color = bpm_color_inactive
bpm_active = False
bpm_text = str(bpm)

beats_per_measure_input_box = pygame.Rect(10, 50, 140, 32)
beats_per_measure_color_inactive = pygame.Color('lightskyblue3')
beats_per_measure_color_active = pygame.Color('dodgerblue2')
beats_per_measure_color = beats_per_measure_color_inactive
beats_per_measure_active = False
beats_per_measure_text = str(beats_per_measure)

measures_per_sequence_input_box = pygame.Rect(10, 90, 140, 32)
measures_per_sequence_color_inactive = pygame.Color('lightskyblue3')
measures_per_sequence_color_active = pygame.Color('dodgerblue2')
measures_per_sequence_color = measures_per_sequence_color_inactive
measures_per_sequence_active = False
measures_per_sequence_text = str(measures_per_sequence)

# Create a Ball object
ball = Ball(screen_width // 2, initial_y, min_radius, max_radius, ball_color)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Cap the frame rate to 60 fps
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if user clicked on any of the input boxes
            if bpm_input_box.collidepoint(event.pos):
                # Toggle BPM input box activity
                bpm_active = not bpm_active
                beats_per_measure_active = False  # Deactivate other input boxes
                measures_per_sequence_active = False
            elif beats_per_measure_input_box.collidepoint(event.pos):
                beats_per_measure_active = not beats_per_measure_active
                bpm_active = False  # Deactivate other input boxes
                measures_per_sequence_active = False
            elif measures_per_sequence_input_box.collidepoint(event.pos):
                measures_per_sequence_active = not measures_per_sequence_active
                bpm_active = False  # Deactivate other input boxes
                beats_per_measure_active = False
            else:
                # Deactivate all input boxes if clicked elsewhere
                bpm_active = False
                beats_per_measure_active = False
                measures_per_sequence_active = False

        elif event.type == pygame.KEYDOWN:
            if bpm_active:
                if event.key == pygame.K_RETURN:
                    try:
                        new_bpm = int(bpm_text)
                        if new_bpm > 0:  # Ensure BPM is positive
                            bpm = new_bpm
                            sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
                    except ValueError:
                        pass  # Ignore invalid input
                elif event.key == pygame.K_BACKSPACE:
                    bpm_text = bpm_text[:-1]
                else:
                    if event.unicode.isdigit():  # Allow only numbers
                        bpm_text += event.unicode
            elif beats_per_measure_active:
                if event.key == pygame.K_RETURN:
                    try:
                        new_beats_per_measure = int(beats_per_measure_text)
                        if new_beats_per_measure > 0:  # Ensure beats_per_measure is positive
                            beats_per_measure = new_beats_per_measure
                            sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
                    except ValueError:
                        pass  # Ignore invalid input
                elif event.key == pygame.K_BACKSPACE:
                    beats_per_measure_text = beats_per_measure_text[:-1]
                else:
                    if event.unicode.isdigit():  # Allow only numbers
                        beats_per_measure_text += event.unicode
            elif measures_per_sequence_active:
                if event.key == pygame.K_RETURN:
                    try:
                        new_measures_per_sequence = int(measures_per_sequence_text)
                        if new_measures_per_sequence > 0:  # Ensure measures_per_sequence is positive
                            measures_per_sequence = new_measures_per_sequence
                            sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
                    except ValueError:
                        pass  # Ignore invalid input
                elif event.key == pygame.K_BACKSPACE:
                    measures_per_sequence_text = measures_per_sequence_text[:-1]
                else:
                    if event.unicode.isdigit():  # Allow only numbers
                        measures_per_sequence_text += event.unicode
            elif event.key == pygame.K_r:  # Press 'r' to start recording
                recording = True
                start_recording_time = time.time()  # Update recording start time at the beginning of recording
                pattern = []
                print("Recording started")  # Indicate recording start
            elif event.key == pygame.K_s:  # Press 's' to stop recording
                recording = False
                print("Recording stopped")  # Indicate recording stop
            elif event.key == pygame.K_UP:  # Increase BPM by 10
                bpm += 10
                sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
            elif event.key == pygame.K_DOWN:  # Decrease BPM by 10
                bpm = max(10, bpm - 10)  # Ensure BPM doesn't go below 10
                sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence

    # Handle MIDI input
    if midi_in and recording:
        for msg in midi_in.iter_pending():
            if msg.type == 'note_on':
                elapsed_time_since_start = time.time() - start_recording_time
                pattern.append(elapsed_time_since_start)
                print(f"Note recorded at {elapsed_time_since_start:.2f} seconds")  # Print recorded note timestamp

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Calculate progress within the sequence (0-1)
    progress = elapsed_time / sequence_duration

    # Calculate measure progress (0-1)
    measure_progress = progress * measures_per_sequence

    # Update the ball
    ball.update(progress, screen_width, screen_height, cycle_count, measures_per_sequence) 

    # Fill the screen with background color
    screen.fill((0, 0, 0))  # Black background

    # Draw the ball
    ball.draw(screen) 

    # Draw the BPM input box
    bpm_txt_surface = font.render(bpm_text, True, bpm_color)
    width = max(180, bpm_txt_surface.get_width()+10)  # Reduce width slightly
    bpm_input_box.w = width
    screen.blit(bpm_txt_surface, (bpm_input_box.x+5, bpm_input_box.y+5))
    pygame.draw.rect(screen, bpm_color, bpm_input_box, 2)

    # Display BPM on screen
    bpm_text_surface = font.render(f"BPM: {bpm}", True, (255, 255, 255))
    bpm_text_rect = bpm_text_surface.get_rect(topleft=(200, 10))  # Adjust x-coordinate
    screen.blit(bpm_text_surface, bpm_text_rect)

    # Draw the Beats Per Measure input box
    beats_per_measure_txt_surface = font.render(beats_per_measure_text, True, beats_per_measure_color)
    width = max(180, beats_per_measure_txt_surface.get_width()+10)  # Reduce width slightly
    beats_per_measure_input_box.w = width
    screen.blit(beats_per_measure_txt_surface, (beats_per_measure_input_box.x+5, beats_per_measure_input_box.y+5))
    pygame.draw.rect(screen, beats_per_measure_color, beats_per_measure_input_box, 2)

    # Display Beats Per Measure on screen
    beats_per_measure_text_surface = font.render(f"BPM/Measure: {beats_per_measure}", True, (255, 255, 255))
    beats_per_measure_text_rect = beats_per_measure_text_surface.get_rect(topleft=(200, 50))  # Adjust x-coordinate
    screen.blit(beats_per_measure_text_surface, beats_per_measure_text_rect)

    # Draw the Measures Per Sequence input box
    measures_per_sequence_txt_surface = font.render(measures_per_sequence_text, True, measures_per_sequence_color)
    width = max(180, measures_per_sequence_txt_surface.get_width()+10)  # Reduce width slightly
    measures_per_sequence_input_box.w = width
    screen.blit(measures_per_sequence_txt_surface, (measures_per_sequence_input_box.x+5, measures_per_sequence_input_box.y+5))
    pygame.draw.rect(screen, measures_per_sequence_color, measures_per_sequence_input_box, 2)

    # Display Measures Per Sequence on screen
    measures_per_sequence_text_surface = font.render(f"Measures/Sequence: {measures_per_sequence}", True, (255, 255, 255))
    measures_per_sequence_text_rect = measures_per_sequence_text_surface.get_rect(topleft=(200, 90))  # Adjust x-coordinate
    screen.blit(measures_per_sequence_text_surface, measures_per_sequence_text_rect)

    # Update the display
    pygame.display.flip()

    # Reset timer and cycle count for next sequence
    if elapsed_time >= sequence_duration:
        start_time = time.time()  # Reset start_time for the next sequence
        cycle_start_time = time.time()  # Reset cycle_start_time at the beginning of each sequence
        cycle_count += 1
        current_measure = 1  # Reset current measure
        print("Recorded pattern:", pattern)  # Print pattern at the start of each sequence
        pattern = []  # Clear the pattern for the next sequence
        start_recording_time = time.time()  # Reset start_recording_time at the beginning of each sequence 

pygame.quit()

# Print the final recorded pattern (if any)
if pattern:
    print("Final recorded pattern:", pattern)
