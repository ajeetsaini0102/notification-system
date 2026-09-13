# Notification System

This project is a simple notification management system where different notifications can be managed and tested from one dashboard.

I built this project using Django REST Framework for the backend and React for the frontend.

## What this project does

The dashboard allows me to manage notifications for two events:

- Login
- Logout

For each event, notifications can be sent through:

- WhatsApp
- Email
- Web Push

From the dashboard I can:

- Create a notification template
- Edit an existing template
- Enable or disable a template
- Test a notification
- Simulate Login and Logout events

## Tech Used

### Backend
- Python
- Django
- Django REST Framework
- SQLite
- WhatsApp Cloud API
- Gmail SMTP
- Web Push

### Frontend
- React
- Vite
- Axios
- CSS

## How it works

The dashboard shows Login and Logout as notification triggers.

For each trigger, there are three notification channels:

| Trigger | WhatsApp | Email | Web Push |
|---------|----------|-------|----------|
| Login | Yes | Yes | Yes |
| Logout | Yes | Yes | Yes |

Each channel has its own template which can be edited, enabled/disabled and tested from the dashboard.

## Dynamic Variables

Templates also support simple dynamic variables.

For example:

```text
Hello {{name}}, you logged in at {{time}}.


Running the project locally
(i) Backend
cd Backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

(ii) Frontend
cd Frontend
npm install
npm run dev

Environment Variables

The backend uses environment variables for notification service credentials such as:

Gmail credentials
WhatsApp API credentials
Web Push/VAPID configuration

The frontend uses the VAPID public key.

For security, .env files and private keys are not included in this repository.

Testing

After starting both the backend and frontend, open the frontend dashboard.

From there you can:

Create or edit a notification template.
Enable the required channel.
Use Test Send to test an individual notification.
Use Simulate Login or Simulate Logout to test the complete notification flow.
Project Structure
Notification-System/
│
├── Backend/
│   ├── config/
│   ├── notifications/
│   ├── manage.py
│   └── Pipfile
│
├── Frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
Notes

This project was built as a full-stack notification system assignment with a focus on managing notification templates and testing multiple notification channels from a single dashboard.

Author

Ajit Singh Saini
