# 📅 Appointment Booking App

A bilingual (Arabic/English) appointment booking web app built with Python and Flask. Clients fill out a form and instantly receive a confirmation email — the business owner gets notified at the same time. Fully configurable for any service business.

![App Screenshot](screenshot.png)

---

## ✨ Features

- **Bilingual UI** — Arabic and English labels throughout
- **Smart time slots** — dropdown of available times, no free-text input
- **Instant emails** — confirmation to client + notification to business owner on every booking
- **Fully configurable** — business name, services, and working hours all set via `.env`
- **Works for any business** — clinics, salons, tutoring centers, dental offices, and more
- **Live deployment** — hosted on PythonAnywhere with a real URL

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Flask |
| Email | Gmail SMTP (smtplib) |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | PythonAnywhere |

---

## 🚀 Live Demo

**[patrickamin.pythonanywhere.com](https://patrickamin.pythonanywhere.com)**

---

## ⚙️ How It Works

1. Client opens the booking page and fills in their details
2. They select a service and an available time slot
3. They hit **Confirm Appointment**
4. Two emails are sent instantly:
   - ✅ Confirmation email to the client
   - 🔔 Notification email to the business owner with all booking details

---

## 🔧 Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/patrickamin/appointment-booking.git
cd appointment-booking
```

### 2. Create virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
BUSINESS_NAME=Cairo Dental Clinic
SERVICES=Consultation,Cleaning,X-Ray,Filling,Whitening

BUSINESS_EMAIL=owner@example.com
GMAIL_USER=your-gmail@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password

SLOT_START=09:00
SLOT_END=17:00
SLOT_INTERVAL=30
```

> **Gmail App Password:** Go to [myaccount.google.com](https://myaccount.google.com) → Security → 2-Step Verification → App passwords. Generate one and paste it here (no spaces).

### 4. Run locally
```bash
PORT=5001 python3.11 app.py
```

Open `http://localhost:5001`

---

## 🔁 Adapting for Any Business

Change just 3 lines in `.env` to deploy for a new client:

```env
BUSINESS_NAME=Layla Beauty Salon
SERVICES=Haircut,Color,Blowout,Keratin
SLOT_START=10:00
SLOT_END=20:00
```

No code changes needed.

---

## 📁 Project Structure

```
appointment-booking/
├── app.py              # Flask backend + email logic
├── templates/
│   └── index.html      # Bilingual booking form
├── requirements.txt
├── .env.example        # Config template
└── render.yaml         # Deployment config
```

---

## 📬 Email Previews

**Client confirmation email**
- Subject: `Appointment Confirmed — [Business Name]`
- Contains: service, date, time, and a thank you message in English + Arabic

**Owner notification email**
- Subject: `New Booking: [Client Name] — [Service] on [Date]`
- Contains: full client details — name, phone, email, service, date, time, notes

---

## 💼 Business Use Case

This project is part of my AI automation agency portfolio. It can be sold as a standalone booking solution for small Egyptian businesses:

- **Setup fee:** $100–200
- **Monthly maintenance:** $30–50/month
- **Customization time:** under 1 hour per new client (just update `.env`)

---

## 👤 Author

**Patrick Amin** — AI Automation Developer  
[github.com/patrickamin](https://github.com/patrickamin)
