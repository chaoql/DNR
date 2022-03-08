import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

from flask import render_template

from application import app


def send_reset_pwd_email(user, re):
    token = user.get_token()
    mail_msg = render_template("mail.html", user=user, token=token)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = app.config['MAIL_USERNAME']
    message['To'] = re[0]
    mail_msg = render_template("mail.html", user=user, token=token)
    subject = '[Chaoql] Reset your password'
    message['Subject'] = Header(subject, "utf-8")
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(app.config['MAIL_SERVER'])
        smtpObj.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        smtpObj.sendmail(app.config['MAIL_USERNAME'], re, message.as_string().encode(encoding='utf-8'))
        app.logger.info("恭喜你!邮件发送成功")
        smtpObj.quit()
    except smtplib.SMTPException as e:
        app.logger.info("Error 无法发送邮件")
        print(e)
