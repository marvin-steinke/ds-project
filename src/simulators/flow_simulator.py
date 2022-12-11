"""
Mosaik interface for the example simulator.

"""
import mosaik_api
from utils.single_model_simulator import SingleModelSimulator # type: ignore

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

class FlowSim(SingleModelSimulator):
    def __init__(self):
        super().__init__(META, FlowModel)

    def step(self, time, inputs, max_advance):
        self.time = time
        model_instance = list(self.entities.values())[0]
        for point_in_time, max_flow in model_instance.max_flows.items():
            if int(point_in_time) == time:
                model_instance.current_max_flow = max_flow
        return time + 1

def main():
    return mosaik_api.start_simulation(FlowSim())
