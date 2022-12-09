"""
This module contains the agent to the consumption controller.
Author: Marvin Steinke

Notes: unts are in KW

"""

class ConsumptionAgent:
    def __init__(self, kW_conversion_factor):
        self.kW_conversion_factor = kW_conversion_factor
        self.drawn = 0
        self.consumption = 0
        self.remaining = 0

    def set_consumption(self, consumption):
        self.consumption = consumption * self.kW_conversion_factor

    def step(self):
        self.remaining = self.consumption - self.drawn
