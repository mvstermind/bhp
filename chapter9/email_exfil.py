import smtplib
import time
import win32con.client

smtp_server = "stmp.example.com"
smtp_port = 587
smtp_acct = "tim@example.com"
smtp_password = "seKret"
tgt_accts = ["tim@elsewhere.com"]


def plain_email(subject, contents):
    message = f"Subject: {subject}\nFrom {smtp_acct}\n"
    message += f"To: {tgt_accts}\n\n{contents.decode()}"
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_acct, smtp_password)

    server.sendmail(smtp_acct, tgt_accts, message)
    time.sleep(1)
    server.quit
