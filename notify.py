# Setting reminders and notifications:
from flask import Flask, request, jsonify,render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import smtplib
import os

# Adding sender's credentials:
EMAIL = os.environ.get("EMAIL")
PASSWD = os.environ.get("PASSWD")

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Store reminders
reminders = []

@app.route("/")
def notify_me():
    return render_template("reminder.html")

def send_reminder(reminder_for, recipient_email):
    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(user=EMAIL, password=PASSWD)

        # Create the message content
        subject = "Reminder Notification"
        body = f"Hi, this is your reminder for: {reminder_for}"
        message = f"Subject: {subject}\n\n{body}"

        smtp.sendmail(
            from_addr=EMAIL,
            to_addrs=recipient_email,
            msg=message
        )
        smtp.quit()
        print(f"Reminder email sent to {recipient_email} for '{reminder_for}'!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    data = request.json
    reminder_for = data['reminder_for']
    reminder_time = data['reminder_time']
    recipient_email = data.get('email', "vedantgunjal2005@gmail.com")  # Use user's email if provided

    # Schedule the reminder
    try:
        time_obj = datetime.strptime(reminder_time, "%H:%M").time()
        scheduler.add_job(
            send_reminder,
            'cron',
            hour=time_obj.hour,
            minute=time_obj.minute,
            args=[reminder_for, recipient_email]
        )
        reminders.append({"reminder_for": reminder_for, "time": reminder_time, "email": recipient_email})
        return jsonify({"message": f"Reminder for '{reminder_for}' set at {reminder_time}!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to set reminder: {e}"}), 400


if __name__ == '__main__':
    app.run(debug=True)
