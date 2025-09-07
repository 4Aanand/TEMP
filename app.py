from flask import Flask, render_template, jsonify, request
import pickle
from sensor import generate_sensor_data

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    sensor = generate_sensor_data()
    prediction = model.predict([[sensor['temperature'], sensor['vibration']]])[0]
    status = 'Alert: Imminent Failure' if prediction == 1 else 'All Good'
    return jsonify({**sensor, 'status': status})

@app.route('/schedule', methods=['POST'])
def schedule():
    repair_time = request.form.get('repair_time')
    print(f"Repair scheduled for: {repair_time}")
    return render_template('index.html', message=f"Repair scheduled for: {repair_time}")

if __name__ == '__main__':
    app.run(debug=True)