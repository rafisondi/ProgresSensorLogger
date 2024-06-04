from hat.sensor import SensorConfig
from hat_proges.https_client import HTTPProgesSensorBox
from hat_proges import ProgesConfig, ProgesSensorBox
from hat.sensor import Measurement
import pandas as pd
from datetime import datetime
import time
import subprocess
import platform

MAX_MEASUREMENT = 1000

def check_connection(sensor : ProgesSensorBox) -> None:
    """ Raises an Exception if cannot ping  Progres Box"""
    if not ping_ok(sensor.config.host):
        raise Exception("Could not connect to host") 
    
def ping_ok(sHost) -> bool:
    try:
        subprocess.check_output(
            "ping -{} 1 {}".format("n" if platform.system().lower() == "windows" else "c", sHost), shell=True
        )
    except Exception:
        return False

class ProgesSensorConfig(SensorConfig):
    rom_id: str
    measurement_type: str

class ProgesSensorMeasurement(Measurement):
    sensor_id: str
    rom_id: str
    channel: int
    value: float
    health: int

class ProgresSensor(HTTPProgesSensorBox):
    def __init__(self,config_box: ProgesConfig,  config: ProgesSensorConfig):
        self.name = config.sensor_id
        self.rom_id = config.rom_id
        self.box = ProgesSensorBox.create_from_config(config_box)
            
    def sample(self) -> ProgesSensorMeasurement:
        try:
            generator = self.box._sample()
            for m in generator:
                if m.sensor_id == self.rom_id:
                    return ProgesSensorMeasurement(
                        sensor_id=self.name,
                        timestamp=m.timestamp,
                        rom_id=self.rom_id,
                        channel=m.channel,
                        value=m.temp,
                        health=m.health
                    )
        except:
            raise TimeoutError("Error: Connection timed out while sampling.")
    
    def _connect(self):
        check_connection(self.box)
        
def save_in_dataframe(m1: ProgesSensorMeasurement, m2: ProgesSensorMeasurement, sensor_table: pd.DataFrame) -> None:
    """Save the measurements into the DataFrame."""
    new_row = {m1.sensor_id: m1.value, m2.sensor_id: m2.value}
    sensor_table.loc[len(sensor_table)] = new_row

def save_to_csv(sensor_table: pd.DataFrame, filename: str) -> None:
    """Save the DataFrame to a CSV file."""
    sensor_table.to_csv(filename, index=False)
        
if __name__ == "__main__":
    config_progres_box=ProgesConfig(
                sensor_id='progres_box', 
                frequency=1, 
                host='192.168.125.69'
            )
    
    progres_sensor_config = ProgesSensorConfig(
            sensor_id= 'REX_Alurahmen_Sensor_1',
            rom_id='DB00000E81526628',
            measurement_type="[T]"
            )
    progres_sensor_config = ProgesSensorConfig(
            sensor_id= 'REX_Alurahmen_Sensor_2',
            rom_id='9300000E80967E28',
            measurement_type="[T]"
            )
    
    progres_sensor_1 = ProgresSensor(config_progres_box, progres_sensor_config)
    progres_sensor_2 = ProgresSensor(config_progres_box, progres_sensor_config)
    
    sensors = [progres_sensor_1 , progres_sensor_2]
    sensors_connected = []
    
    for sensor in sensors: 
        try: 
            sensor._connect()
            sensors_connected.append(sensor)
            status = "Connected"
        except:
            status = "Disconnected"
        
        print(f"{sensor.sensor_id:<25} | {status:<15}")
        
    measurement_table = pd.DataFrame(columns=[sensor.sensor_id for sensor in sensors])
    while True:
        start_time = time.time()
        m1 = progres_sensor_1.sample()
        m2 = progres_sensor_2.sample()
 
        save_in_dataframe(m1, m2, measurement_table)
        
        if len(measurement_table) == MAX_MEASUREMENT:
            current_date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            filename = f"progres_temperature_{current_date}.csv"
            save_to_csv(measurement_table, filename)
            break
            
        

    
    
