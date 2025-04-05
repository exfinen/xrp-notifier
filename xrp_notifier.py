import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import xrpl

XRP_NOTIFIER_GMAIL_ACCOUNT = "XRP_NOTIFIER_GMAIL_ACCOUNT"
XRP_NOTIFIER_GMAIL_PWD = "XRP_NOTIFIER_GMAIL_PWD"
XRP_NOTIFIER_SEND_TO = "XRP_NOTIFIER_SEND_TO"
XRP_NOTIFIER_XRP_ACCOUNT = "XRP_NOTIFIER_XRP_ACCOUNT"

for env_var in [XRP_NOTIFIER_GMAIL_ACCOUNT, XRP_NOTIFIER_GMAIL_PWD, XRP_NOTIFIER_XRP_ACCOUNT, XRP_NOTIFIER_SEND_TO]:
  if os.getenv(env_var) is None:
    print(f"{env_var} is not set")
    exit(1)

def send_email(body):
  global XRP_NOTIFIER_GMAIL_ACCOUNT
  global XRP_NOTIFIER_GMAIL_PWD
  global XRP_NOTIFIER_SEND_TO

  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  sender_email = os.getenv(XRP_NOTIFIER_GMAIL_ACCOUNT)
  app_password = os.getenv(XRP_NOTIFIER_GMAIL_PWD)
  recipient_email = os.getenv(XRP_NOTIFIER_SEND_TO)

  msg = MIMEMultipart()
  msg["From"] = sender_email
  msg["To"] = recipient_email
  msg["Subject"] = "XRP account balance changed"
  msg.attach(MIMEText(body, "plain"))

  try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
  except Exception as e:
    print(f"Failed to send email: {e}")
  finally:
    server.quit()

def get_balance(account):
  client = xrpl.clients.JsonRpcClient("https://s1.ripple.com:51234")
  try:
    balance = xrpl.account.get_balance(account, client)
    return int(balance) / 1_000_000

  except Exception as e:
    return None

last_notified = None
should_notify = False

def start_server():
  global should_notify
  global last_notified
  global XRP_NOTIFIER_XRP_ACCOUNT

  account = os.getenv(XRP_NOTIFIER_XRP_ACCOUNT)

  while True:
    if last_notified is None or should_notify:
      balance = get_balance(account)
      if balance is not None and balance > 10:
        msg = f"Balance: {balance}"
        send_email(msg)
        print(msg)
        last_notified = datetime.now()
        should_notify = False
    else:
      threshold_date = last_notified + timedelta(days=20)
      if datetime.now() > threshold_date:
        should_notify = True

    hour = 60 * 60
    time.sleep(1 * hour)

def start_lambda(_event, _context):
  global should_notify
  global last_notified
  global XRP_NOTIFIER_XRP_ACCOUNT

  account = os.getenv(XRP_NOTIFIER_XRP_ACCOUNT)
  balance = get_balance(account)

  if balance is not None and balance > 10:
    msg = f"Balance: {balance}"
    send_email(msg)

if __name__ == "__main__":
    start_server()

