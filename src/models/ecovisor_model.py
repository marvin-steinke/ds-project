"""
This module contains the Ecovisor model.
Author: Marvin Steinke

"""

from models.simple_battery_model import SimpleBatteryModel # type: ignore
import redis
from redis.commands.json.path import Path

class EcovisorModel:
    def __init__(self, battery_capacity = 10.0, battery_charge_level = -1.0):
        self.battery = SimpleBatteryModel(battery_capacity, battery_charge_level)
        self.energy_grid = SimpleEnergyGridModel(carbon_datafile, carbon_conversion_facor, sim_start)
        self.battery_charge_level = self.battery.charge
        self.battery_charge_rate = 0.0
        self.battery_discharge_rate = 0.0
        self.battery_max_discharge = float('inf')
        self.consumption = 0.0
        self.solar_power = 0.0
        self.grid_carbon = 0.0
        self.grid_power = 0.0
        self.total_carbon = 0.0
        self.container = {}
        self.redis = redis.Redis(host='localhost',port=6379,db=0)
        self.send_redis_update()
        
    def step(self):
        #get updated values from redis
        self.get_redis_update()
        remaining = self.consumption - self.solar_power
        # excess (or equal) solar power
        if remaining <= 0:
            self.battery_discharge_rate = 0
        # solar power is insufficient -> use battery
        else:
            self.battery_discharge_rate = min(self.battery_max_discharge,
                                              self.battery_charge_level * 3600.0,
                                              remaining)
            remaining -= self.battery_discharge_rate
        self.grid_power = self.battery_charge_rate + remaining
        self.battery.delta = self.battery_charge_rate - self.battery_discharge_rate
        self.battery.step()
        self.battery_charge_level = self.battery.charge
        self.energy_grid.step()
        self.grid_carbon = self.energy_grid.carbon
        self.total_carbon = self.grid_carbon * self.grid_power
        # send updated values to redis
        self.send_redis_update()

    # method to update redis data
    # packs values in data struct and sends it to redis
    def send_redis_update(self) -> None:
        data_dict = {
            "solar_power" : self.solar_power,
            "grid_power" : self.grid_power,
            "grid_carbon" : self.grid_carbon,
            "battery_discharge_rate" : self.battery_discharge_rate,
            "battery_charge_level" : self.battery_charge_level,
        }
        self.redis.mset(data_dict)
        self.redis.json().set('container',Path.root_path(),self.container)
    #Gets datastructure from redis and updates the used values (other left commented in code for reference)
    def get_redis_update(self) -> None:
        key_dict = {"solar_power","grid_power","grid_carbon","battery_discharge_rate","battery_charge_level"}
        data_dict = self.redis.mget(key_dict)
        data_dict = dict(zip(key_dict,data_dict))        
        #self.solar_power = float(data_dict["solar_power"])
        #self.grid_power = float(data_dict["grid_power"])
        self.battery_discharge_rate = float(data_dict["battery_discharge_rate"])
        self.battery_charge_level = float(data_dict["battery_charge_level"])
        self.container = self.redis.json().get("container")
        #self.grid_carbon = float(data_dict["grid_carbon"])
        
        #compute total consumption of consumers
        d_values = self.container.values()
        consumption = 0
        for value in d_values:
            consumption = consumption + value
        self.consumption = consumption