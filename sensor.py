import random

def generate_sensor_data():
    return {
        'temperature': round(random.uniform(60, 100), 2),
        'vibration': round(random.uniform(0.2, 1.5), 2)
    }