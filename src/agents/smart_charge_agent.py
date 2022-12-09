"""
This module contains the agent to the smart charge controller.
Author: Marvin Steinke

Notes: units are in kW, power storage in kWh

"""

class SmartChargeAgent:
    def __init__(self, max_flow = float('inf'), available = 100):
        self.max_flow = max_flow
        self.available = available
        self.drawn = 0

    def step(self, request):
        self.drawn = request
        if self.drawn > self.max_flow:
            self.drawn = self.max_flow
        # kWh to kWs conversion
        if self.drawn > self.available * 3600:
            self.drawn = self.available * 3600
