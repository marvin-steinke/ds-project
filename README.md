# ds-project
Integrating Souza et al.'s Ecovisor into Mosaik Co-Simulation
Distributed Systems Project Winter Term 2022/2023

## Repository Structure

```
├── documents: contains all paperwork like presentations, pictures and stuff
├── resources: data for carbon intensity solar generation
└── src
    ├── mwe.py
    ├── agents
    │   ├── consumption_agent.py
    │   └── pv_agent.py
    ├── models
    │   ├── simple_energy_grid_model.py
    │   ├── simple_battery_model.py
    │   └── ecovisor_model.py
    ├── simulators
    │   ├── collector.py
    │   ├── consumption_controller.py
    │   ├── ecovisor.py
    │   └── pv_controller.py
    └── utils
        ├── api_server
        ├── consumer.py
        └── single_model_simulator.py
```

## Further Resources
Mosaik: https://mosaik.offis.de/
Ecovisor: https://arxiv.org/abs/2210.04951
