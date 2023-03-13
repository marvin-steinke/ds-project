# ds-project
Distributed Systems Project Winter Term 2022/2023

## Repository Structure

```
├── documents: contains all paperwork like presentations, pictures and stuff
├── LICENSE
├── README.md
├── resources: data for carbon intensity solar generation
│   ├── actuals.csv
│   ├── carbon_intensity.zip
│   ├── consumption.csv
│   ├── forecasts.csv
│   └── tesing_PV.csv
└── src
    ├── agents
    │   ├── consumption_agent.py
    │   │   ├── consumption_agent.cpython-310.pyc
    │   │   └── smart_charge_agent.cpython-310.pyc
    │   └── smart_charge_agent.py
    ├── models
    │   └── simple_battery_model.py
    ├── scc_mwe.py
    ├── simulators
    │   ├── collector.py
    │   ├── consumption_controller.py
    │   ├── flow_simulator.py
    │   ├── simple_battery_simulator.py
    │   └── smart_charge_controller.py
    └── utils
        └── single_model_simulator.py
```

## Further Resources

Mosaik: https://mosaik.offis.de/

Ecovisor: https://arxiv.org/abs/2210.04951

SymPi: https://simpy.readthedocs.io

MidtermPresentation: https://docs.google.com/presentation/d/1ghZASuAjA9Wq2quv4jdH2l4i-2MHgjfrNF5xFjGLGcU/edit#slide=id.g1aecc6f150d_0_6


## Start Simulation

install dependencys 'pyton -m pip -r requirements.txt'

install & start docker 'systemctl start docker'

start api server 'python api_server.py'

start simulation 'python mwe.py'

start consumer 'python api_consumer.py'

## API usage
The API exposes the following endpoints via http.

The standard url is [localhost:8080/api/*](localhost:8080/api/*)

|Method|Endpoint|Parameter|
|------|--------|---------|
|GET|/api/solar_power|-|
|GET|/api/grid_power|-|
|GET|/api/grid_carbon|-|
|GET|/api/battery_discharge_rate|-|
|GET|/api/battery_charge_level|-|
|GET|/api/container_powercap|container_id:str|
|GET|/api/container_power|container_id:str|
|POST|/api/container_powercap|container_id:str, kW:float|
|POST|/api/battery_charge_level|kW:float|
|POST|/api/battery_max_discharge|kW:float|
