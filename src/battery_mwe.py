import mosaik
import mosaik.util

SIM_CONFIG = {
    'BatterySim': {
        'python': 'simulators.simple_battery_simulator:SimpleBatterySim',
    },
    'Collector': {
        'python': 'simulators.collector:Collector',
    },
}

END = 10

def main():
    world = mosaik.World(SIM_CONFIG) # type: ignore
    create_scenario(world)
    world.run(until=END) # As fast as possilbe

def create_scenario(world):
    # Start simulators
    battery_sim = world.start('BatterySim')
    collector = world.start('Collector')
    # Instantiate models
    battery_model = battery_sim.SimpleBatteryModel()
    monitor = collector.Monitor()
    # Connect entities
    world.connect(battery_model, monitor, 'charge', 'delta')

if __name__ == '__main__':
    main()
