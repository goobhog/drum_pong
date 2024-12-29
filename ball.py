import pygame
import math

class Ball:
  def __init__(self, x, y, min_radius, max_radius, color):
      self.x = x
      self.y = y
      self.min_radius = min_radius
      self.max_radius = max_radius
      self.color = color
      self.radius = min_radius 

  def calculate_horizontal_position(self, progress, screen_width, measures_per_sequence):
      center = screen_width // 2
      amplitude = screen_width // 4
      measure_progress = progress * measures_per_sequence
      return center + amplitude * math.sin(measure_progress * math.pi)

  def calculate_vertical_position(self, progress, screen_height):
      return screen_height * 2 // 3 - (screen_height // 3) * 0.5 * (1 - math.cos(progress * 2 * math.pi))

  def update(self, progress, screen_width, screen_height, cycle_count, measures_per_sequence):
      self.x = self.calculate_horizontal_position(progress, screen_width, measures_per_sequence)
      self.y = self.calculate_vertical_position(progress, screen_height)

  # Calculate size variation smoothly (using a sine wave)
      if cycle_count % 2 == 0:
        self.radius = self.min_radius + (self.max_radius - self.min_radius) * progress
      else:
        self.radius = self.max_radius - (self.max_radius - self.min_radius) * progress

  def draw(self, screen):
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))
