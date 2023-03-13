# ds-project
### Integrating Souza et al.'s Ecovisor into Mosaik Co-Simulation
### Distributed Systems Project Winter Term 2022/2023

To reduce emissions, cloud platforms must increasingly rely on renewable energy
sources such as solar and wind power. Nevertheless, the issue of volatility
associated with these sources presents a significant challenge, since current
energy systems conceal such unreliability in hardware. Souza et al. have
devised a solution to this issue by creating an “ecovisor”. This system
virtualizes the energy infrastructure and allows for software-defined control
to be accessible by applications. Setting up the ecovisor to develop
carbon-aware applications, however, can be costly and time consuming. To
address this problem, we simulated the ecovisor and its virtual energy system
and integrated in into a Mosaik co-simulation. With an API server and a Redis
database we are enabling Software- (SIL) and Hardware-In-The-Loop capabilities.
To evaluate our approach, we created test cases using recorded solar and carbon
data to demonstrate the accuracy of the ecovisor model’s implementation and its
ability to transfer data correctly between the model and the API server.

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

## Start Simulation

install dependencys `python -m pip -r requirements.txt`

install & start docker `systemctl start docker`

start api server `python api_server.py`

start simulation `python mwe.py`

start consumer `python api_consumer.py`

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
