# 1. Add your new app and UI libraries to INSTALLED_APPS
INSTALLED_APPS = [
    # ... default django apps ...
    'crispy_forms',
    'crispy_bootstrap5',
    'dashboard',
]

# 2. Tell Django where to find your global templates
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Must include this directory
        'APP_DIRS': True,
        # ... options ...
    },
]

# 3. Configure Crispy Forms at the bottom of settings.py
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"