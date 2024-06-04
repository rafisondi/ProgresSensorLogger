import csv
import random
from hat.sensor import Measurement
import pandas as pd

MEASUREMENT_CYCLE = 100

class ProgesSensorMeasurement(Measurement):
    sensor_id: str
    rom_id: str
    channel: int
    value: float
    health: int

def generate_fake_measurement(sensor_id: str) -> ProgesSensorMeasurement:
    """Generate a fake measurement."""
    return ProgesSensorMeasurement(
        sensor_id=sensor_id,
        rom_id=f"ROM_{random.randint(1000, 9999)}",
        channel=random.randint(1, 10),
        value=round(random.uniform(0, 100), 2),
        health=random.randint(0, 100)
    )

def save_in_dataframe(m1: ProgesSensorMeasurement, m2: ProgesSensorMeasurement, sensor_table: pd.DataFrame) -> None:
    """Save the measurements into the DataFrame."""
    new_row = {m1.sensor_id: m1.value, m2.sensor_id: m2.value}
    sensor_table.loc[len(sensor_table)] = new_row

def run_measurement_cycle(sensor_table: pd.DataFrame, cycles: int) -> None:
    """Run the measurement cycle for a given number of cycles."""
    for _ in range(cycles):
        measurement_1 = generate_fake_measurement("sensor_1")
        measurement_2 = generate_fake_measurement("sensor_2")
        save_in_dataframe(measurement_1, measurement_2, sensor_table)

def save_to_csv(sensor_table: pd.DataFrame, filename: str) -> None:
    """Save the DataFrame to a CSV file."""
    sensor_table.to_csv(filename, index=False)
    
    
if __name__ == "__main__":
    sensor_table = pd.DataFrame(columns=["sensor_1", "sensor_2"])
    
    # Run the measurement cycle
    run_measurement_cycle(sensor_table, MEASUREMENT_CYCLE)
    
    # Save the resulting DataFrame to a CSV file
    save_to_csv(sensor_table, 'file.csv')

    # Optional: Print the DataFrame to verify
    print(sensor_table)