from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

reset_codes = {}

@app.route('/')
def home():
    return "Server is running!"

@app.route('/send-reset-code', methods=['POST'])
def send_reset_code():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    code = str(random.randint(100000, 999999))
    reset_codes[email] = {'code': code, 'expires': datetime.utcnow() + timedelta(minutes=5)}

    try:
        send_email(email, code)
        return jsonify({'message': 'Reset code sent successfully'})
    except Exception as e:
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500

@app.route('/verify-reset-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if email in reset_codes:
        entry = reset_codes[email]
        if entry['code'] == code and datetime.utcnow() < entry['expires']:
            return jsonify({'message': 'Code verified successfully'})
        else:
            return jsonify({'message': 'Invalid or expired code'}), 400
    else:
        return jsonify({'message': 'No reset code found for this email'}), 404

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if email and new_password:
        return jsonify({'message': f'Password for {email} reset successfully'})
    else:
        return jsonify({'message': 'Missing email or new password'}), 400

def send_email(to_email, code):
    sender = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    msg = MIMEText(f"Your password reset code is: {code}")
    msg['Subject'] = 'Password Reset Code'
    msg['From'] = sender
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.send_message(msg)