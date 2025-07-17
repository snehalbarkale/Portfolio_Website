from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template, redirect, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_dev_key")
load_dotenv()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/projects')
def projects():
    return render_template("projects.html")


@app.route('/resume')
def resume():
    return render_template("resume.html")


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    subject = f"Message from {name}"
    body = f"From: {name} <{email}>\n\nMessage:\n{message}"

    sender_email = os.environ.get("EMAIL_USER")  # your Gmail
    password = os.environ.get("EMAIL_PASS")  # app password (NOT your real Gmail password)
    receiver_email = sender_email  # you’ll receive the message at same address

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        flash("✅ Message sent successfully!", "success")
    except Exception as e:
        print("Error:", e)
        flash("❌ Failed to send message.", "danger")

    return redirect("/contact")


if __name__ == '__main__':
    app.run(debug=True)
