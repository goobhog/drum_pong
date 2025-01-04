import pygame
import mido
from mido import MidiFile
from pygame.locals import *

class OstinatoCreator:
    def __init__(self):
        self.is_running = False
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ostinato Creator")

##        # MIDI setup
##        try:
##            self.midi_in = mido.open_input()
##            print(f"Using MIDI input: {self.midi_in.name}") 
##        except:
##            print("No MIDI input devices found.")
##            self.midi_in = None

        self.midi_out = mido.open_output()

        # Recording variables
        self.recording_active = False
        self.recording_start_time = 0
        self.recorded_notes = [] 

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle MIDI input
                if self.midi_in and event.type == mido.MidiMessage: 
                    if self.recording_active:
                        self.handle_midi_message(msg) 

            # ... (Handle other events like keyboard input, UI interactions) ...

            # Update display
            self.screen.fill((255, 255, 255)) 
            # ... (Draw UI elements) ...
            pygame.display.flip()

        pygame.quit()

    def handle_midi_message(self, msg):
        if self.recording_active:
            if msg.type == 'note_on' and msg.velocity > 0: 
                # Record note-on event with timestamp
                self.recorded_notes.append((msg, pygame.time.get_ticks())) 
            elif msg.type == 'note_off':
                # Find the corresponding note-on event
                for i, (note_on_msg, note_on_time) in enumerate(self.recorded_notes):
                    if note_on_msg.note == msg.note and note_on_msg.channel == msg.channel:
                        note_duration = pygame.time.get_ticks() - note_on_time
                        self.recorded_notes[i] = (note_on_msg, note_duration) 
                        break 

    def play_ostinato(self):
        for note_data in self.recorded_notes:
            note_on_msg, duration = note_data
            self.midi_out.send(note_on_msg)
            time.sleep(duration / 1000)  # Simple playback, consider using a timer
            note_off_msg = mido.Message('note_off', note=note_on_msg.note, velocity=0, channel=note_on_msg.channel)
            self.midi_out.send(note_off_msg)

# ... (Rest of the class implementation: UI elements, saving/loading, etc.) ...

