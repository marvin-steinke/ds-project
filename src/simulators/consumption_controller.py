"""
Mosaik interface for the simple battery simulator.
Author: Marvin Steinke

Notes: *discharge_s* is specified in Ws since the consumption is modeled per second

"""

import mosaik_api
from agents.consumption_agent import ConsumptionAgent # type: ignore

META = {
    'type': 'event-based',
    'models': {
        'ConsumptionAgent': {
            'public': True,
            'params': [],
            'attrs': ['drawn', 'consumption', 'remaining'],
        },
    },
}

class ConsumptionController(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'ConsumptionAgent_'
        self.agents = {}
        self.time = 0

    def init(self, sid, time_resolution, eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError(f'ConsumptionAgent only supports time_resolution=1., but {time_resolution} was set.')
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.agents)
        entities = []
        for i in range(next_eid, next_eid + num):
            agent_instance = ConsumptionAgent()
            eid = self.eid_prefix + str(i)
            self.agents[eid] = agent_instance
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        for agent_eid, attrs in inputs.items():
            agent = self.agents[agent_eid]
            consumption_dict = attrs.get('consumption', {})
            if len(consumption_dict) > 0:
                agent.consumption = list(consumption_dict.values())[0]
                continue
            drawn_dict = attrs.get('drawn', {})
            if len(drawn_dict) > 0:
                agent.drawn = list(drawn_dict.values())[0]
                agent.step()
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
    return mosaik_api.start_simulation(ConsumptionController())
