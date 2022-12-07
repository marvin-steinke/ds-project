"""
Smart charge controller adapted from the Ecovisor architecture. Acts as medium
between a consumer and producer by restricting power flow.
Author: Marvin Steinke

"""

import mosaik_api

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
        self.agents = []
        self.time = 0
        self.max_flow = {}
        self.drawn = {}
        self.available = {}
        self.drawn = {}

    def create(self, num, model):
        n_agents = len(self.agents)
        entities = []
        for i in range(n_agents, n_agents + num):
            eid = 'SmartChargeAgent_%d' % i
            self.max_flow[eid] = float('inf')
            self.available[eid] = float('inf')
            self.agents.append(eid)
            entities.append({'eid': eid, 'type': model})
        return entities

    def handle_request(self, agent_eid, request):
        available = self.available[agent_eid]
        max_flow = self.max_flow[agent_eid]
        drawn = request
        if drawn > max_flow:
            drawn = max_flow
        if drawn > available:
            drawn = available
        self.drawn[agent_eid] = drawn

    def step(self, time, inputs, max_advance):
        self.time = time
        for agent_eid, attrs in inputs.items():
            request_dict = attrs.get('request', {})
            if len(request_dict) > 0:
                request = list(request_dict.values())[0]
                self.handle_request(agent_eid, request)
                continue
            available_dict = attrs.get('available', {})
            if len(request_dict) > 0:
                self.available[agent_eid] = list(available_dict.values())[0]
                continue
            max_flow_dict = attrs.get('max_flow', {})
            if len(request_dict) > 0:
                self.max_flow[agent_eid] = list(max_flow_dict.values())[0]
                continue
        return None

    def get_data(self, outputs):
        data = {}
        for agent_eid, attrs in outputs.items():
            for attr in attrs:
                if attr == 'max_flow':
                    if agent_eid in self.max_flow:
                        data[agent_eid]['max_flow'] = self.max_flow[agent_eid]
                if attr == 'drawn':
                    if agent_eid in self.drawn:
                        data[agent_eid]['drawn'] = self.drawn[agent_eid]
                data['time'] = self.time
        return data

def main():
    return mosaik_api.start_simulation(SmartChargeController())
