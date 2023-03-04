"""
This module contains the Ecovisor model.
Author: Marvin Steinke

"""

from models.simple_battery_model import SimpleBatteryModel # type: ignore
from models.simple_energy_grid_model import SimpleEnergyGridModel # type: ignore

class EcovisorModel:
    def __init__(self, carbon_datafile, carbon_conversion_facor=1, sim_start=0, battery_capacity = 10, battery_charge_level = -1):
        self.battery = SimpleBatteryModel(battery_capacity, battery_charge_level)
        self.energy_grid = SimpleEnergyGridModel(carbon_datafile, carbon_conversion_facor, sim_start)
        self.battery_charge_level = self.battery.charge
        self.battery_charge_rate = 0
        self.battery_discharge_rate = 0
        self.battery_max_discharge = float('inf')
        self.consumption = 0
        self.solar_power = 0
        self.grid_carbon = 0
        self.grid_power = 0
        self.total_carbon = 0

    def step(self) -> None:
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
        self.battery.delta = self.battery_charge_rate - self.battery_discharge_rate
        self.battery.step()
        self.battery_charge_level = self.battery.charge
        self.energy_grid.step()
        self.grid_carbon = self.energy_grid.carbon
        self.total_carbon = self.grid_carbon * self.grid_power
