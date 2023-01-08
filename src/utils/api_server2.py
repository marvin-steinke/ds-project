from fastapi import FastAPI, Form
import uvicorn
import redis
from redis.commands.json.path import Path

class ApiServer:
    def __init__(self):
        self.redis = redis.Redis(host='localhost',port=6379,db=0)
        self.run()

    def get_solar_power(self) -> float:
        solar_power = self.redis.get("solar_power")
        return float(solar_power)

    def get_grid_power(self) -> float:
        grid_power = self.redis.get("grid_power")
        return float(grid_power)

    def get_grid_carbon(self) -> float:
        grid_carbon = self.redis.get("grid_carbon")
        return float(grid_carbon)

    def get_battery_discharge_rate(self) -> float:
        battery_discharge_rate = self.redis.get("battery_discharge_rate")
        return float(battery_discharge_rate)

    def get_battery_charge_level(self) -> float:
        battery_charge_level = self.redis.get("battery_charge_level")
        return float(battery_charge_level)

    def get_container_powercap(self, container_id) -> float:
        return self.container[container_id]

    def set_container_powercap(self, container_id, kW):
        self.container.update({container_id : kW})

    def set_battery_charge_level(self, kW):
        self.battery_charge_level = kW

    def set_battery_max_discharge(self, kW):
        self.battery_max_discharge = kW

    @property
    def app(self) -> FastAPI:
        app = FastAPI()

        #get_solar_power
        @app.get('/api/solar_power')
        async def get_solar_power():
            kW = self.get_solar_power()
            return { "kW" : kW}

        #get_grid_power
        @app.get('/api/grid_power')
        async def get_grid_power():
            kW = self.get_grid_power()
            return {'kW' : kW}

        #get_grid_carbon
        @app.get('/api/grid_carbon')
        async def get_grid_carbon():
            co2 = self.get_grid_carbon()
            return {'g*co_2/kW' : co2}

        #get_battery_discharge_rate
        @app.get('/api/battery_discharge_rate')
        async def battery_discharge_rate():
            kW = self.get_battery_discharge_rate()
            return {'kW' : kW}

        #get_battery_charge_level
        @app.get('/api/battery_charge_level')
        async def battery_charge_level():
            kW = self.get_battery_charge_level()
            return {'kW' : kW}

        #get_container_powercap
        @app.get('/api/container_powercap')
        async def container_powercap(container_id : str = Form(...)):
            try:
                kW = self.set_container_powercap(container_id)
            except:
                return {'An error occured!'}
            return {container_id + 'kW' : kW}

        #get_container_power
        @app.get('/api/container_power')
        async def container_power(container_id : str = Form(...)):
            kW = self.get_contaner_powercap(container_id)
            return { container_id + ' KW' : kW}

        #set container power cap
        @app.post("/api/container_powercap")
        async def container_powercap(self,container_id : str = Form(...), kW : float = Form(...)):
            try:
                self.set_container_powercap(container_id, kW)
            except:
                return {'An error occured!'}
            return{'Fine'}

        #set battery_charge_rate
        @app.post("/api/battery_charge_level")
        async def battery_charge_level(kW : float = Form(...)):
            try:
                self.set_battery_charge_level(kW)
            except:
                return {'An error occured!'}
            return{'Fine'}

        #set battery_max_discharge
        @app.post("/api/battery_max_discharge")
        async def battery_max_discharge(kW : float = Form(...)):
            try:
                self.set_battery_max_discharge(kW)
            except:
                return {'An error occured!'}
            return{'Fine'}

        #additional inti method if needed
        #app.on_event("startup")(self._init)
        return app

    def run(self, port = None) -> None:
        uvicorn.run(self.app, host="127.0.0.1", port=port or 8080)

# For test purpose!

#app = lambda: a.app

if __name__ == '__main__':
    a = ApiServer()
    