from flask import render_template, current_app
from flask_mail import Message


def send_email(to, subject, template, **kwargs):
    msg = Message(
        current_app.config['ONELOVE_MAIL_SUBJECT_PREFIX'] + subject,
        sender=current_app.config['ONELOVE_MAIL_SENDER'],
        recipients=[to],
    )
    msg.html = render_template(template + '.html', **kwargs)
    current_app.onelove.mail.send(msg)
