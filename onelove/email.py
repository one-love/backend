from flask import current_app, render_template
from flask.ext.mail import Message
from onelove import OneLove

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['ONELOVE_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['ONELOVE_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    OneLove.mail.send(msg)
