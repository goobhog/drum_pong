import pygame
import math
import time
import mido
from pygame.locals import *
from ball import Ball
from input_handler import InputHandler

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

# Create a Ball object
ball = Ball(screen_width // 2, initial_y, min_radius, max_radius, ball_color)

# Create an instance of InputHandler()
input_handler = InputHandler()

# Default game parameters
bpm = 120
beats_per_measure = 4
measures_per_sequence = 4

# Calculate sequence duration in seconds
sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence

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

# Define input box rectangles
bpm_input_box = pygame.Rect(10, 10, 140, 32)
beats_per_measure_input_box = pygame.Rect(10, 50, 140, 32)
measures_per_sequence_input_box = pygame.Rect(10, 90, 140, 32)

# Initial values for input boxes
bpm_active = True  # Start with BPM input box active
beats_per_measure_active = False
measures_per_sequence_active = False

# Initialize text for input boxes
bpm_text = str(bpm)
beats_per_measure_text = str(beats_per_measure)
measures_per_sequence_text = str(measures_per_sequence)

def draw_input_box(screen, value, box, active):
    """Draws a text input box on the screen.

    Args:
        screen: The Pygame display surface.
        value: The current value of the input.
        box: The pygame.Rect object representing the input box.
        active: Whether the input box is currently active.
    """
    color = 'dodgerblue2' if active else 'lightskyblue3'
    txt_surface = font.render(str(value), True, color)
    width = 180  # Set a fixed width for the input box
    box.w = width
    screen.blit(txt_surface, (box.x+5, box.y+5))
    pygame.draw.rect(screen, color, box, 2)

    # Display the label below the input box
    txt_surface = font.render(f"BPM: {value}" if box == bpm_input_box else 
                             f"Beats/Measure: {value}" if box == beats_per_measure_input_box else 
                             f"Measures/Sequence: {value}", True, (255, 255, 255))
    txt_rect = txt_surface.get_rect(topleft=(200, box.y))
    screen.blit(txt_surface, txt_rect)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Cap the frame rate to 60 fps
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if user clicked on any of the input boxes
            if bpm_input_box.collidepoint(event.pos):
                bpm_active = True
                beats_per_measure_active = False
                measures_per_sequence_active = False
            elif beats_per_measure_input_box.collidepoint(event.pos):
                bpm_active = False
                beats_per_measure_active = True
                measures_per_sequence_active = False
            elif measures_per_sequence_input_box.collidepoint(event.pos):
                bpm_active = False
                beats_per_measure_active = False
                measures_per_sequence_active = True
            else:
                bpm_active = False
                beats_per_measure_active = False
                measures_per_sequence_active = False

        # Get user input for BPM, beats_per_measure, and measures_per_sequence
        if event.type == pygame.KEYDOWN:
            if bpm_active:
                bpm_text, enter_pressed = input_handler.get_integer_input(bpm_text, event)
                if enter_pressed:
                    try:
                        bpm = int(bpm_text)
                        if bpm > 0:
                            sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
                    except ValueError:
                        pass
            elif beats_per_measure_active:
                beats_per_measure_text, enter_pressed = input_handler.get_integer_input(beats_per_measure_text, event)
                if enter_pressed:
                    try:
                        beats_per_measure = int(beats_per_measure_text)
                        if beats_per_measure > 0:
                            sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
                    except ValueError:
                        pass
            elif measures_per_sequence_active:
                measures_per_sequence_text, enter_pressed = input_handler.get_integer_input(measures_per_sequence_text, event)
                if enter_pressed:
                    try:
                        measures_per_sequence = int(measures_per_sequence_text)
                        if measures_per_sequence > 0:
                            sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence
                    except ValueError:
                        pass

        # Handle BPM adjustment (using the InputHandler)
        new_bpm, bpm_adjusted = input_handler.handle_bpm_adjustment(bpm, event, dt)

        # Handle BPM adjustment (from your existing code)
##        if event.type == pygame.KEYDOWN:
##            if event.key == pygame.K_UP:
##                bpm += 10
##                bpm_text = str(bpm)
##            elif event.key == pygame.K_DOWN:
##                bpm = max(10, bpm - 10)
##                bpm_text = str(bpm)

        # Update BPM if it was adjusted
        if bpm_adjusted:
            bpm = new_bpm 

    # Recalculate sequence duration in seconds
    sequence_duration = 60 / bpm * beats_per_measure * measures_per_sequence

    # Handle other game events (e.g., key presses)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:  # Press 'r' to start recording
            recording = True
            start_recording_time = time.time()  # Update recording start time
            pattern = []
            print("Recording started")  # Indicate recording start
        elif event.key == pygame.K_s:  # Press 's' to stop recording
            recording = False
            print("Recording stopped")  # Indicate recording stop


    # Handle MIDI input
    if midi_in and recording:
        for msg in midi_in.iter_pending():
            if msg.type == 'note_on':
                elapsed_time_since_start = time.time() - start_recording_time
                pattern.append(elapsed_time_since_start)

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

    # Draw input boxes using the draw_input_box function
    draw_input_box(screen, bpm_text, bpm_input_box, bpm_active)
    draw_input_box(screen, beats_per_measure_text, beats_per_measure_input_box, beats_per_measure_active)
    draw_input_box(screen, measures_per_sequence_text, measures_per_sequence_input_box, measures_per_sequence_active)

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
