import unittest
import math
from ball import Ball

class TestBall(unittest.TestCase):
    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600
        self.cycle_count = 16
        self.measures_per_sequence = 4
        self.ball = Ball(self.screen_width // 2, self.screen_height // 2, 10, 50, (255, 0, 0))

    def test_initial_radius(self):
        self.assertEqual(self.ball.radius, 10, "Initial radius should be equal to min_radius")

    def test_horizontal_position(self):
        progress = 0.5
        expected_x = self.ball.calculate_horizontal_position(progress, self.screen_width, self.measures_per_sequence)
        self.assertAlmostEqual(expected_x, self.screen_width // 2, places=2, msg="Horizontal position should be at center at progress 0.5") 

    def test_vertical_position(self):
        progress = 0.5
        expected_y = self.screen_height * 2 // 3 - (self.screen_height // 3) * 0.5 * (1 - math.cos(progress * 2 * math.pi)) 
        actual_y = self.ball.calculate_vertical_position(progress, self.screen_height)
        self.assertAlmostEqual(actual_y, expected_y, places=2, msg="Vertical position should match the calculation at progress 0.5")

    def test_radius_variation_cycle_even(self):
        progress = 0.75
        cycle_count = 0  # Set cycle_count to even
        self.ball.update(progress, self.screen_width, self.screen_height, cycle_count, self.measures_per_sequence)
        expected_radius = 10 + (50 - 10) * 0.75  # Assuming linear interpolation based on progress
        self.assertAlmostEqual(self.ball.radius, expected_radius, places=2, msg="Radius should increase in even cycle")

    def test_radius_variation_cycle_odd(self):
        progress = 0.75
        cycle_count = 1  # Set cycle_count to odd
        self.ball.update(progress, self.screen_width, self.screen_height, cycle_count, self.measures_per_sequence)
        expected_radius = 50 - (50 - 10) * 0.75  # Assuming linear interpolation based on progress
        self.assertAlmostEqual(self.ball.radius, expected_radius, places=2, msg="Radius should decrease in odd cycle")

if __name__ == '__main__':
    unittest.main()
