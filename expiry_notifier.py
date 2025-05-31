import json
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv
from prefect import flow, task

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
NOTIFY_TO = "ralfs.kanders@gmail.com"

@task
def load_products():
    with open("products.json", "r") as file:
        return json.load(file)

@task
def send_email(product_name, expiry_date):
    msg = EmailMessage()
    msg["Subject"] = f"⏰ Reminder: {product_name} expires tomorrow!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = NOTIFY_TO
    msg.set_content(f"The product '{product_name}' will expire on {expiry_date}.\nCheck your inventory!")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent for {product_name}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

@task
def check_and_notify(products):
    today = datetime.now().date()
    for product in products:
        expiry_date = datetime.strptime(product["expiry_date"], "%Y-%m-%d").date()
        if expiry_date - today == timedelta(days=1):
            send_email(product["name"], product["expiry_date"])

@flow(name="Product Expiry Notifier")
def expiry_notifier_flow():
    products = load_products()
    check_and_notify(products)

if __name__ == "__main__":
    expiry_notifier_flow()
