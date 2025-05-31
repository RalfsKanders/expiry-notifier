from datetime import datetime, timedelta
import json
import smtplib
from email.message import EmailMessage
from prefect import flow, task
import os

YOUR_EMAIL = "kristofersrudzats0@gmail.com"
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = "ralfs.kanders@gmail.com"

@task
def load_products(filepath="products.json"):
    with open(filepath, "r") as file:
        return json.load(file)

@task
def send_email(product_name, expiry_date):
    msg = EmailMessage()
    msg["Subject"] = f"⚠️ {product_name} expires tomorrow!"
    msg["From"] = YOUR_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(f"Reminder: {product_name} will expire on {expiry_date}. Please use it soon!")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(YOUR_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent for {product_name}.")
    except Exception as e:
        print("❌ Failed to send email:", e)

@task
def check_and_notify(products):
    today = datetime.today().date()
    for product in products:
        try:
            expiry = datetime.strptime(product["expiry_date"], "%Y-%m-%d").date()
            if expiry - today == timedelta(days=1):
                send_email(product["name"], product["expiry_date"])
        except ValueError:
            print(f"⚠️ Invalid date format for: {product['name']}")

@flow(name="Product Expiry Notifier")
def expiry_notifier():
    products = load_products()
    check_and_notify(products)

if __name__ == "__main__":
    expiry_notifier()
