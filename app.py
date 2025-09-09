from flask import Flask, render_template, jsonify, request,redirect

import pickle
from sensor import generate_sensor_data
from notifier import send_sms, send_email
import smtplib
from email.mime.text import MIMEText
from predictor import is_failure, get_risk_level
from datetime import datetime





app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/data')
# def data():
#     machine_id = request.args.get('machine_id', 'MCH-001')
#     machine_name = 'Compressor A' if machine_id == 'MCH-001' else 'Pump B'

#     sensor = generate_sensor_data()

#     try:
#         prediction = model.predict([[sensor['temperature'], sensor['vibration']]])[0]
#         status = 'Alert: Imminent Failure' if prediction == 1 else 'All Good'
#     except Exception as e:
#         print(f"Prediction error: {e}")
#         return jsonify({'error': 'Prediction failed'}), 500

#     if status == 'Alert: Imminent Failure':
#         alert_msg = (
#             f"⚠️ {machine_name} ({machine_id}) is at risk of failure.\n"
#             f"Temperature: {sensor['temperature']}°F\n"
#             f"Vibration: {sensor['vibration']}g"
#         )
#         send_sms('+916306677603', alert_msg)
#         send_email('aanand6306677603@gmail.com', f'Failure Alert: {machine_name}', alert_msg)

#     return jsonify({**sensor, 'status': status})


# @app.route('/schedule', methods=['POST'])
# def schedule():
#     repair_time = request.form.get('repair_time')
#     print(f"Repair scheduled for: {repair_time}")
#     return render_template('index.html', message=f"Repair scheduled for: {repair_time}")

# scheduled_data = {}
# @app.route('/scheduled', methods=['POST'])
# def store_schedule():
#     global scheduled_data
#     scheduled_data = {
#         'machine_name': request.form['machineName'],
#         'machine_id': request.form['machineId'],
#         'schedule_date': request.form['scheduleDate']
#     }
#     return redirect('/')

# @app.route('/send-email', methods=['POST'])
# def send_email_route():
#     recipient = request.form['email']
#     subject = "Maintenance Scheduled for Your Machine"
#     body = f"""
#     Dear Repair Team,

#     A maintenance check has been scheduled for the following machine:

#     Machine Name: {scheduled_data.get('machine_name')}
#     Machine ID: {scheduled_data.get('machine_id')}
#     Scheduled Date: {scheduled_data.get('schedule_date')}
# Please confirm availability or reach out for rescheduling.

#     Regards,
#     Predictive Maintenance System
#     """

#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = 'aanand6306677603@gmail.com'  # Replace with your sender email
#     msg['To'] = recipient

#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login('aanand6306677603@gmail.com', 'your-app-password')  # Use app password if Gmail
#             server.send_message(msg)
#         return "Email sent successfully!"
#     except Exception as e:
#         return f"Failed to send email: {e}"


@app.route('/data')
def data():
    machine_id = request.args.get('machine_id', 'MCH-001')
    machine_name = 'Compressor A' if machine_id == 'MCH-001' else 'Pump B'

    sensor = generate_sensor_data()

    try:
        failure, prob = is_failure(sensor)
        risk = get_risk_level(prob)
        status = 'Alert: Imminent Failure' if failure else 'All Good'
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

    # Trigger alerts
    if failure:
        alert_msg = (
            f"⚠️ {machine_name} ({machine_id}) is at risk of failure.\n"
            f"Temperature: {sensor['temperature']}°F\n"
            f"Vibration: {sensor['vibration']}g\n"
            f"Risk Level: {risk} ({round(prob * 100, 2)}%)"
        )
        send_sms('+916306677603', alert_msg)
        send_email('aanand6306677603@gmail.com', f'Failure Alert: {machine_name}', alert_msg)

    # Auto-schedule if risk is high or critical
    global scheduled_data
    if risk in ['🟠 High', '🔴 Critical']:
        scheduled_data = {
            'machine_name': machine_name,
            'machine_id': machine_id,
            'schedule_date': datetime.now().strftime('%Y-%m-%d')
        }

        # Optional: notify repair company immediately
        auto_email_body = f"""
        Dear Repair Team,

        A maintenance check has been auto-scheduled due to high risk detection:

        Machine Name: {scheduled_data['machine_name']}
        Machine ID: {scheduled_data['machine_id']}
        Scheduled Date: {scheduled_data['schedule_date']}
        Risk Level: {risk}
        Failure Probability: {round(prob * 100, 2)}%

        Please confirm availability or reach out for rescheduling.

        Regards,
        Predictive Maintenance System
        """
        msg = MIMEText(auto_email_body)
        msg['Subject'] = f"Auto-Scheduled Maintenance: {machine_name}"
        msg['From'] = 'aanand6306677603@gmail.com'
        msg['To'] = 'repairteam@example.com'  # Replace with actual recipient

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('aanand6306677603@gmail.com', 'your-app-password')
                server.send_message(msg)
        except Exception as e:
            print(f"Auto-schedule email failed: {e}")

    return jsonify({
        **sensor,
        'status': status,
        'failure_probability': round(prob * 100, 2),
        'risk_level': risk
    })


if __name__ == '__main__':
    app.run(debug=True)