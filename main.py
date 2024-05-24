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
        config=ProgesConfig( sensor_id="Box1", frequency= 3, host="192.168.125.69"),
    )
    sensor.measure_for_duration(duration=10)

    measurements = sensor.list_measurements()
    for m in measurements:
        id = m.sensor_id
        time = m.timestamp
        temp = m.temp
        # Save in corresponding list as touple entry
        measurements_dict[id].append( (time, temp))
    print(f"{'-'*80}")
    print(measurements_dict[SENSOR_ID_1])
    print(f"{'-'*80}")
    print(measurements_dict[SENSOR_ID_2])
    
    sensor.disconnect()
    

    
        