import smtplib
from email.mime.text import MIMEText
from config import EMAIL, APP_PASSWORD, RECIPIENT


def send_email(html_content):

    msg = MIMEText(html_content, 'html')

    msg['Subject'] = 'Daily Market Dashboard'
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)

    server.quit()