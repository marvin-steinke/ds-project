"""
Mosaik interface for the simple battery simulator.
Author: Marvin Steinke

Notes: *discharge_s* is specified in Ws since the consumption is modeled per second

"""

import mosaik_api
from models.simple_battery_model import SimpleBatteryModel # type: ignore

META = {
    'type': 'event-based',
    'models': {
        'SimpleBatteryModel': {
            'public': True,
            'params': ['capacity', 'init_charge'],
            'attrs': ['capacity', 'charge', 'discharge_s'],
        },
    },
}

class SimpleBatterySim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Battery_'
        self.entities = {}  # Maps EIDs to model instances/entities
        self.time = 0

    def init(self, sid, time_resolution, eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError(f'SimpleBatterySim only supports time_resolution=1., but {time_resolution} was set.')
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, capacity = 100, init_charge = -1):
        next_eid = len(self.entities)
        entities = []
        for i in range(next_eid, next_eid + num):
            model_instance = SimpleBatteryModel(capacity, init_charge)
            eid = self.eid_prefix + str(i)
            self.entities[eid] = model_instance
            entities.append({'eid': eid, 'type': model})
        return entities

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

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.entities[eid]
            data['time'] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['SimpleBatteryModel']['attrs']: # type: ignore
                    raise ValueError(f'Unknown output attribute: {attr}')
                data[eid][attr] = getattr(model, attr)
        return data

def main():
    return mosaik_api.start_simulation(SimpleBatterySim())
