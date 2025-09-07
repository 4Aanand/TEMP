import random

def generate_sensor_data():
    # 40% chance to simulate failure-prone values
    if random.random() < 0.4:
        temperature = round(random.uniform(95, 110), 2)
        vibration = round(random.uniform(1.3, 2.0), 2)
    else:
        temperature = round(random.uniform(60, 90), 2)
        vibration = round(random.uniform(0.2, 1.0), 2)

    return {
        'temperature': temperature,
        'vibration': vibration
    }
