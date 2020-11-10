import smtplib
from email.mime.text import MIMEText
import random
from . import settings

def send_email(receive):
    msg_from = settings.FROM_EMAIL
    pwd = settings.EMAIL_PASSWORD
    msg_to = receive

    code = get_code()
    subject = 'Reshub'
    content = '您的验证码是：'+str(code)
    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = msg_from
    message['To'] = msg_to

    s = smtplib.SMTP_SSL("smtp.qq.com",465)#邮件服务器及端口号
    try:
        s.login(msg_from, pwd)
        s.sendmail(msg_from, msg_to, message.as_string())
        s.quit()
        return True, code
    except Exception:
        s.quit()
        return False, code

def get_code():
    return random.randint(111111, 999999)