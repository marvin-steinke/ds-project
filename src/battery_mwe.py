import mosaik
import mosaik.util

SIM_CONFIG = {
    'CSV': {
        'python': 'mosaik_csv:CSV',
        },
    'BatterySim': {
        'python': 'simulators.simple_battery_simulator:SimpleBatterySim',
        },
    'Collector': {
        'python': 'simulators.collector:Collector',
        },
    'ConsumptionController': {
        'python': 'simulators.consumption_controller:ConsumptionController',
        },
    'SmartChargeController': {
        'python': 'simulators.smart_charge_controller:SmartChargeController',
        },
}

START = '2014-01-01 00:00:00'
CONSUMPTION_DATA = '../resources/consumption.csv'
END = 10

def main():
    world = mosaik.World(SIM_CONFIG) # type: ignore
    create_scenario(world)
    world.run(until=END)

def create_scenario(world):
    # Start simulators
    battery_sim = world.start('BatterySim')
    collector = world.start('Collector')
    consumption_sim = world.start('CSV', sim_start=START, datafile=CONSUMPTION_DATA)
    consumption_controller = world.start('ConsumptionController')
    smart_charge_controller = world.start('SmartChargeController')
    # Instantiate models
    battery_capacity = 10
    battery_model = battery_sim.SimpleBatteryModel(capacity = battery_capacity)
    consumption_model = consumption_sim.Consumption()
    consumption_agent = consumption_controller.ConsumptionAgent(kW_conversion_factor = 0.001)
    smart_charge_agent = smart_charge_controller.SmartChargeAgent(available = battery_capacity)
    monitor = collector.Monitor()
    # Connect entities
    ## Consumer -> ConsumerAgent:
    world.connect(consumption_model, consumption_agent, ('P', 'consumption'))
    ## SmartChargeAgent <-> ConsumptionAgent
    world.connect(consumption_agent, smart_charge_agent, ('consumption', 'request'))
    world.connect(smart_charge_agent, consumption_agent, 'drawn', weak = True)
    ## BatteryModel <-> SmartChargeAgent
    world.connect(battery_model, smart_charge_agent, ('charge', 'available'))
    world.connect(smart_charge_agent, battery_model, ('drawn', 'discharge_s'), weak = True)
    # Monitor
    world.connect(battery_model, monitor, 'charge', 'discharge_s')
    world.connect(smart_charge_agent, monitor, 'available', 'drawn')
    world.connect(consumption_agent, monitor, 'consumption', 'drawn')

if __name__ == '__main__':
    main()
