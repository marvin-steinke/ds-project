"""
This module contains the agent to the consumption controller.
Author: Marvin Steinke

"""

class ConsumptionAgent:
    def __init__(self):
        self.drawn = 0
        self.consumption = 0
        self.remaining = 0

    def step(self):
        self.remaining = self.consumption - self.drawn
