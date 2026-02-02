from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template, redirect, flash, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_dev_key")
load_dotenv()

print("EMAIL:", os.getenv("EMAIL_ADDRESS"))
print("PASS:", os.getenv("EMAIL_PASSWORD"))
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


@app.route("/send-message", methods=["POST"])
def send_message():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(
                os.environ.get("EMAIL_ADDRESS"),
                os.environ.get("EMAIL_PASSWORD")
            )
            connection.sendmail(
                from_addr=os.environ.get("EMAIL_ADDRESS"),
                to_addrs=os.environ.get("EMAIL_ADDRESS"),
                msg=f"Subject:New Portfolio Message\n\nName: {name}\nEmail: {email}\nMessage: {message}"
            )

        flash("Message sent successfully!", "success")

    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again later.", "danger")

    return redirect(url_for("contact"))


if __name__ == '__main__':
    app.run(debug=True)
