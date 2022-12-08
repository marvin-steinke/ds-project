"""
Smart charge controller adapted from the Ecovisor architecture. Acts as medium
between a consumer and producer by restricting power flow.
Author: Marvin Steinke

"""

import mosaik_api
from agents.smart_charge_agent import SmartChargeAgent # type: ignore

META = {
    'type': 'event-based',
    'models': {
        'SmartChargeAgent': {
            'public': True,
            'params': [],
            'attrs': ['request', 'max_flow', 'available', 'drawn'],
        },
    },
}

class SmartChargeController(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'SmartChargeAgent_'
        self.agents = {}
        self.time = 0
        self.max_flow = {}
        self.drawn = {}
        self.available = {}

    def init(self, sid, time_resolution, eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError(f'SmartChargeController only supports time_resolution=1., but {time_resolution} was set.')
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.agents)
        entities = []
        for i in range(next_eid, next_eid + num):
            model_instance = SmartChargeAgent()
            eid = self.eid_prefix + str(i)
            self.agents[eid] = model_instance
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        for agent_eid, attrs in inputs.items():
            agent = self.agents[agent_eid]
            request_dict = attrs.get('request', {})
            if len(request_dict) > 0:
                request = list(request_dict.values())[0]
                agent.step(request)
                continue
            available_dict = attrs.get('available', {})
            if len(request_dict) > 0:
                agent.available = list(available_dict.values())[0]
                continue
            max_flow_dict = attrs.get('max_flow', {})
            if len(request_dict) > 0:
                agent.max_flow = list(max_flow_dict.values())[0]
                continue
        return None

    def get_data(self, outputs):
        data = {}
        for agent_eid, attrs in outputs.items():
            agent = self.agents[agent_eid]
            data['time'] = self.time
            data[agent_eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['SmartChargeAgent']['attrs']: # type: ignore
                    raise ValueError(f'Unknown output attribute: {attr}')
                data[agent_eid][attr] = getattr(agent, attr)
        return data

def main():
    return mosaik_api.start_simulation(SmartChargeController())
