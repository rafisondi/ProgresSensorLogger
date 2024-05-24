from hat_proges import ProgesConfig, ProgesSensorBox


SENSOR_ID_1 = 'DB00000E81526628'
SENSOR_ID_2 = '9300000E80967E28'

measurements_dict = {
  SENSOR_ID_1: [],
  SENSOR_ID_2: []    
}

if __name__ == "__main__":
    
    
    # without calibration
    sensor = ProgesSensorBox.create_from_config(
        config=ProgesConfig( sensor_id="Box1", frequency= 1, host="192.168.125.69"),
    )
    
    num_of_sensors = 2 
    sensor.measure_for_count(count = 4 * num_of_sensors)
    measurements = sensor.list_measurements()
    for m in measurements:
        id = m.sensor_id
        time = m.timestamp
        temp = m.temp
        # Save in corresponding list as touple entry
        measurements_dict[id].append( (time, temp))
    
    print("\n")
    print(f"{'-'*80}")
    print(f'{measurements_dict[SENSOR_ID_1] = }')
    print(f"{'-'*80}")
    print(f'{measurements_dict[SENSOR_ID_2] = }')
    print("\n")
    
    sensor.disconnect()
    

    
        