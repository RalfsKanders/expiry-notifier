import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = "kristofersrudzats0@gmail.com"
EMAIL_PASSWORD = "rudzatsgejs1"

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("Logged in successfully!")
except Exception as e:
    print("Failed to login:", e)
