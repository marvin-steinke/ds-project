"""
Mosaik interface for the simple battery simulator.
Author: Marvin Steinke

Notes: *delta* is specified in kWs since the consumption is modeled per second

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
            'attrs': ['capacity', 'charge', 'delta'],
        },
    },
}

class SimpleBatterySim(SingleModelSimulator):
    def __init__(self):
        super().__init__(META, SimpleBatteryModel)

def main():
    return mosaik_api.start_simulation(SimpleBatterySim())
