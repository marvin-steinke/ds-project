"""
Smart charge controller adapted from the Ecovisor architecture. Acts as medium
between a consumer and producer by restricting power flow.
Author: Marvin Steinke

"""

import mosaik_api
from agents.smart_charge_agent import SmartChargeAgent # type: ignore
from utils.single_model_simulator import SingleModelSimulator # type: ignore

META = {
    'type': 'event-based',
    'models': {
        'SmartChargeAgent': {
            'public': True,
            'params': ['max_flow', 'available'],
            'attrs': ['request', 'max_flow', 'available', 'drawn'],
        },
    },
}

class SmartChargeController(SingleModelSimulator):
    def __init__(self):
        super().__init__(META, SmartChargeAgent)

    def step(self, time, inputs, max_advance):
        self.time = time
        for agent_eid, attrs in inputs.items():
            agent = self.entities[agent_eid]
            max_flow_dict = attrs.get('max_flow', {})
            if len(max_flow_dict) > 0:
                agent.max_flow = list(max_flow_dict.values())[0]
            available_dict = attrs.get('available', {})
            if len(available_dict) > 0:
                agent.available = list(available_dict.values())[0]
                del agent.drawn
                continue
            request_dict = attrs.get('request', {})
            if len(request_dict) > 0:
                request = list(request_dict.values())[0]
                agent.step(request)
        return None

def main():
    return mosaik_api.start_simulation(SmartChargeController())
