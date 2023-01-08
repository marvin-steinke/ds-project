from fastapi import FastAPI, Form
import uvicorn
import sys
import redis
from redis.commands.json.path import Path

HOST = 'localhost'
PORT = 8080

app = FastAPI()

# starts the Server @HOST:PORT (standard localhost:8080)
def start_server(host='localhost',port=8080):
    try:
        uvicorn.run(app, host=host, port=port, log_level="debug" )
    except Exception as e:
        print(e,file=sys.stderr)

def get_solar_power() -> float:
    pass

def get_grid_power() -> float:
    pass

def get_grid_carbon() -> float:
    pass

def get_battery_discharge_rate():
    pass

def get_battery_charge_level():
    pass

def set_container_powercap(container_id):
    pass

def get_contaner_powercap(container_id):
    pass

def set_battery_charge_level(kW):
    pass

def set_battery_max_discharge(kW):
    pass

@app.get('/api/solar_power')
async def get_solar_power():
    kW = get_solar_power()
    return { "kW" : kW}

#get_grid_power
@app.get('/api/grid_power')
async def get_grid_power():
    kW = get_grid_power()
    return {'kW' : kW}

#get_grid_carbon
@app.get('/api/grid_carbon')
async def get_grid_carbon():
    co2 = get_grid_carbon()
    return {'g*co_2/kW' : co2}

#get_battery_discharge_rate
@app.get('/api/battery_discharge_rate')
async def battery_discharge_rate():
    kW = get_battery_discharge_rate()
    return {'kW' : kW}

#get_battery_charge_level
@app.get('/api/battery_charge_level')
async def battery_charge_level():
    kW = get_battery_charge_level()
    return {'kW' : kW}

#get_container_powercap
@app.get('/api/container_powercap')
async def container_powercap(container_id : str = Form(...)):
    try:
        kW = set_container_powercap(container_id)
    except:
        return {'An error occured!'}
    return {container_id + 'kW' : kW}

#get_container_power
@app.get('/api/container_power')
async def container_power(container_id : str = Form(...)):
    kW = get_contaner_powercap(container_id)
    return { container_id + ' KW' : kW}

#set container power cap
@app.post("/api/container_powercap")
async def container_powercap(self,container_id : str = Form(...), kW : float = Form(...)):
    try:
        set_container_powercap(container_id, kW)
    except:
        return {'An error occured!'}
    return{'Fine'}

#set battery_charge_rate
@app.post("/api/battery_charge_level")
async def battery_charge_level(kW : float = Form(...)):
    try:
        set_battery_charge_level(kW)
    except:
        return {'An error occured!'}
    return{'Fine'}

#set battery_max_discharge
@app.post("/api/battery_max_discharge")
async def battery_max_discharge(kW : float = Form(...)):
    try:
        set_battery_max_discharge(kW)
    except:
        return {'An error occured!'}
    return{'Fine'}

