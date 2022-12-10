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
}

START = '2014-01-01 00:00:00'
CONSUMPTION_DATA = '../resources/consumption.csv'
END = 10

def main():
    world = mosaik.World(SIM_CONFIG) # type: ignore
    create_scenario(world)
    world.run(until=END) # As fast as possilbe

def create_scenario(world):
    # Start simulators
    battery_sim = world.start('BatterySim')
    collector = world.start('Collector')
    consumption_sim = world.start('CSV', sim_start=START, datafile=CONSUMPTION_DATA)
    # Instantiate models
    battery_model = battery_sim.SimpleBatteryModel()
    consumption_model = consumption_sim.Consumption()
    monitor = collector.Monitor()
    # Connect entities
    world.connect(consumption_model, battery_model, ('P', 'discharge_s'))
    world.connect(battery_model, monitor, 'charge', 'discharge_s')
    world.connect(consumption_model, monitor, 'P')

if __name__ == '__main__':
    main()
