from hat_proges import ProgesConfig, ProgesSensorBox, ProgesMeasurement

import subprocess
import platform
import json
from typing import List, Dict

sensor_dict = {
    'DB00000E81526628' : [],
    '9300000E80967E28' : []
}

def load_sensor_ids_to_dict(json_file_path) -> dict:
    with open(json_file_path, 'r') as file:
        config = json.load(file)
    
    sensor_ids = config.get("sensor_ids", [])
    measurements_dict = {sensor_id: [] for sensor_id in sensor_ids}
    
    return measurements_dict

def extract_sensor_measurement(measurement_list : List[ProgesMeasurement], sensor_dict: Dict) -> None:
    for m in measurement_list:
        id = m.sensor_id
        time = m.timestamp
        temp = m.temp
        # Save in corresponding list as touple entry
        sensor_dict[id].append( (time, temp))
        
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

    return True
if __name__ == "__main__":
    
    num_of_sensors = 2 
    num_of_measurements_per_sensor = 4
    file_path = "./sensors/sensor_id.json"
    
    sensors_dict  = load_sensor_ids_to_dict(file_path)
    
    sensor = ProgesSensorBox.create_from_config(
        config=ProgesConfig( sensor_id="Box1", frequency= 1, host="192.168.125.69"),
    )
      
    check_connection(sensor)
    print("Connected")
    
    sensor.measure_for_count(count = num_of_measurements_per_sensor * num_of_sensors)
    print("Measured")
    
    measurements = sensor.list_measurements()
    sensor.stop_measuring()
    
    extract_sensor_measurement(measurements , sensors_dict)
    
    print("\n")
    for id in sensors_dict:
        print(f"{'-'*80}")
        print(id + ": ",  sensors_dict[id])
    print("\n")
    
    sensor.disconnect()
    

    
        