import smtplib
from email.mime.text import MIMEText

from ..settings_service import get_setting


def send_mail(db, to: str, subject: str, body: str):
    host = get_setting(db, 'email', 'smtp_host', '')
    port = int(get_setting(db, 'email', 'smtp_port', '587') or 587)
    username = get_setting(db, 'email', 'smtp_username', '')
    password = get_setting(db, 'email', 'smtp_password', '')
    sender = get_setting(db, 'email', 'sender_email', username)
    use_tls = get_setting(db, 'email', 'use_tls', 'true').lower() == 'true'
    if not host or not sender:
        raise RuntimeError('Missing email SMTP settings')
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    with smtplib.SMTP(host, port, timeout=20) as smtp:
        if use_tls:
            smtp.starttls()
        if username:
            smtp.login(username, password)
        smtp.send_message(msg)
    return {'status': 'sent', 'to': to, 'subject': subject, 'sender': sender}
