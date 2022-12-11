"""
Generic class for single-model simulators or controllers.
Author: Marvin Steinke

"""

import mosaik_api

class SingleModelSimulator(mosaik_api.Simulator):
    def __init__(self, META, model_class):
        super().__init__(META)
        self.eid_prefix = list(self.meta['models'])[0] + '_' # type: ignore
        self.model_class = model_class
        self.entities = {}
        self.time = 0

    def init(self, sid, time_resolution, eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError(f'{self.__class__.__name__} only supports time_resolution=1., but {time_resolution} was set.')
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, *args, **kwargs):
        next_eid = len(self.entities)
        entities = []
        for i in range(next_eid, next_eid + num):
            model_instance = self.model_class(*args, **kwargs)
            eid = self.eid_prefix + str(i)
            self.entities[eid] = model_instance
            entities.append({'eid': eid, 'type': model})
        return entities

    def get_data(self, outputs):
        data = {}
        model_name = list(self.meta['models'])[0] # type:ignore
        for eid, attrs in outputs.items():
            model = self.entities[eid]
            data['time'] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models'][model_name]['attrs']: # type: ignore
                    raise ValueError(f'Unknown output attribute: {attr}')
                if hasattr(model, attr):
                    data[eid][attr] = getattr(model, attr)
        return data
