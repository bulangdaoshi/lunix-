from random import Random

from django.core.mail import send_mail , EmailMultiAlternatives

from Users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+= chars[random.randint(0,length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title= ''
    email_body = ''

    if send_type == 'register':
        email_title = 'python学习在线网注册激活链接'
        email_body = '<a href="http://127.0.0.1:8000/users/active/{0}">请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}</a>'.format(code)

        send_status = EmailMultiAlternatives(email_title,email_body,EMAIL_FROM,[email])

        send_status.attach_alternative(email_body,'text/html')

        send_status.send()

    elif send_type == 'forget':
        email_title = 'python学习在线网注册找回密码'
        email_body = '<a href="http://127.0.0.1:8000/users/reset/{0}">请点击下面的链接找回你的密码:http://127.0.0.1:8000/reset/{0}</a>'.format(
            code)

        send_status = EmailMultiAlternatives(email_title, email_body, EMAIL_FROM, [email])

        send_status.attach_alternative(email_body, 'text/html')

        send_status.send()
