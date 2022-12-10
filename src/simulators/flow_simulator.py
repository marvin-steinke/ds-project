"""
Mosaik interface for the example simulator.

"""
from logging import currentframe
import mosaik_api

META = {
    'type': 'time-based',
    'models': {
        'FlowModel': {
            'public': True,
            'params': ['max_flows'],
            'attrs': ['current_max_flow'],
        },
    },
}

class FlowModel:
    def __init__(self, max_flows, current_max_flow = float('inf')):
        self.max_flows = max_flows
        self.current_max_flow = current_max_flow

class FlowSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Model_'
        self.entities = {}  # Maps EIDs to model instances/entities
        self.time = 0

    def init(self, sid, time_resolution, eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError(f'FlowSim only supports time_resolution=1., but {time_resolution} was set.')
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, max_flows):
        if num > 1 or len(self.entities) > 0:
            raise RuntimeError('Can only create one instance of FlowSim.')
        entities = []
        model_instance = FlowModel(max_flows)
        eid = self.eid_prefix + '0'
        self.entities[eid] = model_instance
        entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        model_instance = list(self.entities.values())[0]
        for point_in_time, max_flow in model_instance.max_flows.items():
            if int(point_in_time) == time:
                model_instance.current_max_flow = max_flow
        return time + 1

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.entities[eid]
            data['time'] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['FlowModel']['attrs']: # type: ignore
                    raise ValueError(f'Unknown output attribute: {attr}')
                data[eid][attr] = getattr(model, attr)
        return data

def main():
    return mosaik_api.start_simulation(FlowSim())
