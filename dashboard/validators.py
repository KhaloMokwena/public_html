import os

from django.core.exceptions import ValidationError

MAX_CV_BYTES = 5 * 1024 * 1024   # same 5MB limit as the old career_handler.php

# First bytes of each allowed format, so a renamed file (e.g. virus.exe -> cv.pdf) is refused.
_SIGNATURES = {
    '.pdf': (b'%PDF',),
    '.docx': (b'PK\x03\x04',),
    '.doc': (b'\xd0\xcf\x11\xe0',),
}


def validate_cv_size(file):
    if file.size > MAX_CV_BYTES:
        raise ValidationError("The CV is too large. Please upload a file of 5 MB or less.")


def validate_cv_signature(file):
    extension = os.path.splitext(file.name)[1].lower()
    signatures = _SIGNATURES.get(extension)
    if not signatures:
        return  # the extension validator reports unsupported types
    head = file.read(8)
    file.seek(0)
    if not any(head.startswith(sig) for sig in signatures):
        raise ValidationError("This file does not look like a genuine PDF, DOC or DOCX document.")
