"""
This module contains the agent to the smart charge controller.
Author: Marvin Steinke

"""

class SmartChargeAgent:
    def __init__(self):
        self.max_flow = float('inf')
        self.available = float('inf')
        self.drawn = 0

    def step(self, request):
        self.drawn = request
        if self.drawn > self.max_flow:
            self.drawn = self.max_flow
        if self.drawn > self.available:
            self.drawn = self.available
