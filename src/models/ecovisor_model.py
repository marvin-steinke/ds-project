"""
This module contains the Ecovisor model.
Author: Marvin Steinke

"""

class EcovisorModel:
    def __init__(self, battery_charge_level):
        self.consumption = 0
        self.battery_charge_rate = 0
        self.battery_discharge_rate = 0
        self.battery_max_discharge = float('inf')
        self.battery_charge_level = battery_charge_level
        self.battery_delta = 0
        self.solar_power = 0
        self.grid_carbon = 0
        self.grid_power = 0
        self.total_carbon = 0

    def step(self):
        remaining = self.consumption - self.solar_power
        # excess (or equal) solar power
        if remaining <= 0:
            self.battery_discharge_rate = 0
        # solar power is insufficient -> use battery
        else:
            self.battery_discharge_rate = min(self.battery_max_discharge,
                                              self.battery_charge_level * 3600,
                                              remaining)
            remaining -= self.battery_discharge_rate
        self.grid_power = self.battery_charge_rate + remaining
        self.battery_delta = self.battery_charge_rate - self.battery_discharge_rate
        self.total_carbon = self.grid_carbon * self.grid_power
