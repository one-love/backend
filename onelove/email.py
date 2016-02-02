from flask import render_template
from flask_mail import Message
from onelove import current_app


def send_email(to, subject, template, **kwargs):
    msg = Message(
        current_app.app.config['ONELOVE_MAIL_SUBJECT_PREFIX'] + subject,
        sender=current_app.app.config['ONELOVE_MAIL_SENDER'],
        recipients=[to],
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    current_app.mail.send(msg)
