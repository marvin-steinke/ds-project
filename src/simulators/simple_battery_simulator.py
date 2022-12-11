"""
Mosaik interface for the simple battery simulator.
Author: Marvin Steinke

Notes: *discharge_s* is specified in Ws since the consumption is modeled per second

"""

import mosaik_api
from models.simple_battery_model import SimpleBatteryModel # type: ignore
from utils.single_model_simulator import SingleModelSimulator # type: ignore

META = {
    'type': 'event-based',
    'models': {
        'SimpleBatteryModel': {
            'public': True,
            'params': ['capacity', 'charge'],
            'attrs': ['capacity', 'charge', 'discharge_s'],
        },
    },
}

class SimpleBatterySim(SingleModelSimulator):
    def __init__(self):
        super().__init__(META, SimpleBatteryModel)

    def step(self, time, inputs, max_advance):
        self.time = time
        # Check for new discharge_s and do step for each model instance:
        for eid, model_instance in self.entities.items():
            if eid in inputs:
                attrs = inputs[eid]
                new_discharge_s = 0
                for attr, values in attrs.items():
                    new_discharge_s = sum(values.values())
                model_instance.discharge_s = new_discharge_s
            model_instance.step()
        return None

def main():
    return mosaik_api.start_simulation(SimpleBatterySim())
