"""
Email notifications for new applications and contact enquiries (the job the old career_handler.php /
contact_handler.php did).

The submission is ALWAYS saved to the database first. Email is a convenience on top: if the mail server
is not configured or is down, the error is logged and the visitor still sees a normal success page,
and nothing is lost because everything is in /manage/.
"""
import logging
import mimetypes
import os

from django.core.mail import EmailMessage
from django.db import DatabaseError

from .content import default_for
from .models import ContentBlock

logger = logging.getLogger(__name__)


def page_value(page, key):
    """Current value of a /manage/ text block (the edit if there is one, else the default)."""
    try:
        value = ContentBlock.objects.filter(page=page, key=key).values_list('value', flat=True).first()
    except DatabaseError:
        value = None
    return value or default_for(page, key)


_block = page_value   # short alias used elsewhere in this module


def _one_line(text):
    """Email subjects must not contain line breaks (header injection)."""
    return ' '.join(str(text).split())


def _send(message):
    try:
        message.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Could not send notification email %r", message.subject)
        return False


def notify_application(application):
    """Email HR the new application with the CV attached. Returns True if it was sent."""
    body = (
        f"Position Applied For: {application.role}\n"
        f"Applicant Name: {application.name}\n"
        f"Email Address: {application.email}\n"
        f"Contact Number: {application.phone}\n"
        f"POPIA agreement accepted: {'Yes' if application.popia_consent else 'No'}\n\n"
        f"Cover Note / Summary:\n{application.message or '(none)'}\n\n"
        f"This application is also saved in the website's Applications inbox (/manage/applications/).\n"
    )
    message = EmailMessage(
        subject=_one_line(f"Job Application: {application.role} - {application.name}"),
        body=body,
        to=[_block('careers', 'apply_email')],
        reply_to=[application.email],
    )
    try:
        with application.cv.open('rb') as handle:
            content = handle.read()
        filename = os.path.basename(application.cv.name)
        message.attach(filename, content, mimetypes.guess_type(filename)[0] or 'application/octet-stream')
    except Exception:
        logger.exception("Could not attach the CV to the notification email")
    return _send(message)


def notify_contact(enquiry):
    """Email the general inbox a new contact enquiry. Returns True if it was sent."""
    body = (
        f"Name: {enquiry.name}\n"
        f"Email: {enquiry.email}\n"
        f"Phone: {enquiry.phone or '(not given)'}\n\n"
        f"Message:\n{enquiry.message}\n"
    )
    message = EmailMessage(
        subject=_one_line(f"General Inquiry from: {enquiry.name}"),
        body=body,
        to=[_block('contact', 'intake_value')],
        reply_to=[enquiry.email],
    )
    return _send(message)
