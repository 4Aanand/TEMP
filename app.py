from flask import Flask, render_template, jsonify, request
import pickle
from sensor import generate_sensor_data
from notifier import send_sms, send_email

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    machine_id = request.args.get('machine_id', 'MCH-001')
    machine_name = 'Compressor A' if machine_id == 'MCH-001' else 'Pump B'

    sensor = generate_sensor_data()

    try:
        prediction = model.predict([[sensor['temperature'], sensor['vibration']]])[0]
        status = 'Alert: Imminent Failure' if prediction == 1 else 'All Good'
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

    if status == 'Alert: Imminent Failure':
        alert_msg = (
            f"⚠️ {machine_name} ({machine_id}) is at risk of failure.\n"
            f"Temperature: {sensor['temperature']}°F\n"
            f"Vibration: {sensor['vibration']}g"
        )
        send_sms('+916306677603', alert_msg)
        send_email('aanand6306677603@gmail.com', f'Failure Alert: {machine_name}', alert_msg)

    return jsonify({**sensor, 'status': status})

@app.route('/schedule', methods=['POST'])
def schedule():
    repair_time = request.form.get('repair_time')
    print(f"Repair scheduled for: {repair_time}")
    return render_template('index.html', message=f"Repair scheduled for: {repair_time}")

if __name__ == '__main__':
    app.run(debug=True)