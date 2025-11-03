import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv("myEmail")
my_pass = os.getenv("myPass")

def create_transporter():
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587 

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(my_email, my_pass)

        print("✅ Transporter connected successfully.")
        return server
    except Exception as e:
        print("❌ Error creating transporter:", e)
        return None

def send_email(to_email, subject, message):
    server = create_transporter()
    if not server:
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = my_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server.send_message(msg)
        print(f"📨 Email sent to {to_email}")
    except Exception as e:
        print("❌ Failed to send email:", e)
    finally:
        server.quit()

if __name__ == "__main__":
    send_email("magretjumbe19@gmail.com", "Hello emailing myself from python", "897780")