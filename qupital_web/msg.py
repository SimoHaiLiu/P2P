import smtplib
from email.mime.text import MIMEText
from filter import receivable_auctions_filter
import time
from flask_mail import Message
from flask import render_template
from init import mail

from_email = 'wmltyq@qq.com'


def email_notification(to_email, passing_all_criteria_auction_no, passing_the_critical_criteria_auction_no):
    msg = MIMEText(
        '<html><body><h1>Passing all criteria auction no.</h1><p>{}</p><h1>Passing the critical criteria auction no.</h1><p>{}</p></body></html>'.format(passing_all_criteria_auction_no, passing_the_critical_criteria_auction_no),
        'html', 'utf-8')
    msg['From'] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Qupital hava receivable auctions"

    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    # server.set_debuglevel(1)
    # xxxxxxxxx 是在QQ邮箱获取的授权码, 如果不需要授权的邮箱直接输入密码即可
    server.login(from_email, "cfafqtnudfoydhcb")
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()


def send_email(to, subject, template, user, token):
    msg = Message(subject, sender=from_email, recipients=[to])
    msg.html = render_template(template + '.txt', user=user, token=token)
    mail.send(msg)


if __name__ == '__main__':
    # email_notification('3081515830@qq.com', ['AC172', 'AC721'])
    passing_all_criteria_auction_no_temp = []
    passing_the_critical_criteria_auction_no_temp = []

    while True:
        try:
            passing_all_criteria, passing_the_critical_criteria = receivable_auctions_filter()
        except Exception as e:
            print('Send email error: {}'.format(e))

        # print(passing_all_criteria)
        # print(passing_the_critical_criteria)

        passing_all_criteria_auction_no = [item['auction_no'] for item in passing_all_criteria]
        passing_the_critical_criteria_auction_no = [item['auction_no'] for item in passing_the_critical_criteria]
        # 只有当数据有变动的时候才发送邮件
        if passing_all_criteria_auction_no_temp != passing_all_criteria_auction_no and passing_the_critical_criteria_auction_no_temp != passing_the_critical_criteria_auction_no:
            email_notification('3081515830@qq.com', passing_all_criteria_auction_no, passing_the_critical_criteria_auction_no)
            passing_all_criteria_auction_no_temp = passing_all_criteria_auction_no
            passing_the_critical_criteria_auction_no_temp = passing_the_critical_criteria_auction_no

        time.sleep(1)
