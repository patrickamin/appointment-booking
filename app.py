from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'My Business')
BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
SERVICES = os.getenv('SERVICES', 'Consultation,Follow-up,General Appointment').split(',')
SLOT_START = os.getenv('SLOT_START', '09:00')
SLOT_END = os.getenv('SLOT_END', '17:00')
SLOT_INTERVAL = int(os.getenv('SLOT_INTERVAL', '30'))


def generate_time_slots():
    start = datetime.strptime(SLOT_START, '%H:%M')
    end = datetime.strptime(SLOT_END, '%H:%M')
    slots = []
    current = start
    while current < end:
        slots.append(current.strftime('%I:%M %p'))  # e.g. 09:00 AM
        current += timedelta(minutes=SLOT_INTERVAL)
    return slots


@app.route('/')
def index():
    return render_template('index.html', business_name=BUSINESS_NAME, services=SERVICES, time_slots=generate_time_slots())


@app.route('/book', methods=['POST'])
def book():
    data = request.json
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    service = data.get('service', '').strip()
    date = data.get('date', '').strip()
    time = data.get('time', '').strip()
    notes = data.get('notes', '').strip()

    if not all([name, phone, email, service, date, time]):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    try:
        send_confirmation(name, email, service, date, time)
        send_notification(name, phone, email, service, date, time, notes)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def send_email(to, msg):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to, msg.as_string())


def send_confirmation(name, email, service, date, time):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Appointment Confirmed — {BUSINESS_NAME}'
    msg['From'] = GMAIL_USER
    msg['To'] = email

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:32px;background:#f9f9f9;border-radius:12px">
      <h2 style="color:#1a7a4a;margin-bottom:4px">Appointment Confirmed ✓</h2>
      <p style="color:#555;margin-top:0">تم تأكيد موعدك</p>
      <hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0">
      <p style="color:#333">Dear <strong>{name}</strong>,</p>
      <p style="color:#333">Your appointment at <strong>{BUSINESS_NAME}</strong> is confirmed.</p>
      <table style="width:100%;border-collapse:collapse;margin:20px 0">
        <tr><td style="padding:8px 0;color:#888;width:120px">Service</td><td style="padding:8px 0;color:#333;font-weight:600">{service}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Date</td><td style="padding:8px 0;color:#333;font-weight:600">{date}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Time</td><td style="padding:8px 0;color:#333;font-weight:600">{time}</td></tr>
      </table>
      <p style="color:#555;font-size:14px">We look forward to seeing you. If you need to reschedule, please contact us.</p>
      <hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0">
      <p style="color:#aaa;font-size:12px;text-align:center">{BUSINESS_NAME}</p>
    </div>
    """
    msg.attach(MIMEText(html, 'html'))
    send_email(email, msg)


def send_notification(name, phone, email, service, date, time, notes):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'New Booking: {name} — {service} on {date}'
    msg['From'] = GMAIL_USER
    msg['To'] = BUSINESS_EMAIL

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:32px;background:#f9f9f9;border-radius:12px">
      <h2 style="color:#1a4a7a;margin-bottom:4px">New Appointment Booked</h2>
      <hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0">
      <table style="width:100%;border-collapse:collapse">
        <tr><td style="padding:8px 0;color:#888;width:100px">Name</td><td style="padding:8px 0;color:#333;font-weight:600">{name}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Phone</td><td style="padding:8px 0;color:#333;font-weight:600">{phone}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Email</td><td style="padding:8px 0;color:#333;font-weight:600">{email}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Service</td><td style="padding:8px 0;color:#333;font-weight:600">{service}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Date</td><td style="padding:8px 0;color:#333;font-weight:600">{date}</td></tr>
        <tr><td style="padding:8px 0;color:#888">Time</td><td style="padding:8px 0;color:#333;font-weight:600">{time}</td></tr>
        <tr><td style="padding:8px 0;color:#888;vertical-align:top">Notes</td><td style="padding:8px 0;color:#333">{notes or '—'}</td></tr>
      </table>
    </div>
    """
    msg.attach(MIMEText(html, 'html'))
    send_email(BUSINESS_EMAIL, msg)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
