from django import forms
from .models import Record, Service, JobPosting, Faq, Division, ContactMessage, ContentBlock, JobApplication
from .content import PAGES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


def media_queryset():
    """Media library items that actually have an image."""
    return Record.objects.exclude(image='').exclude(image__isnull=True).order_by('-created_at')


class MediaChoiceField(forms.ModelChoiceField):
    """Dropdown over the media library. Shows the id so identical titles can be told apart."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('queryset', media_queryset())
        kwargs.setdefault('required', False)
        kwargs.setdefault('empty_label', '— none —')
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return f"{obj.title} (#{obj.pk})"


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'description', 'image', 'show_in_gallery']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Explicit Save Button styled with Bootstrap
        self.helper.add_input(Submit('submit', 'Save to Media library', css_class='btn btn-success w-100 mt-3'))


# --- Page text and media editor (one form per page, built from dashboard/content.py) ---

class PageContentForm(forms.Form):
    """
    One field per block on a page, pre-filled with the current value.
    Text blocks: saving a field back to its default (or clearing it) removes the override.
    Media blocks: a dropdown over the media library; "none" removes the override.
    """

    def __init__(self, page_slug, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_slug = page_slug
        self.blocks = PAGES[page_slug]['blocks']
        overrides = dict(ContentBlock.objects.filter(page=page_slug).values_list('key', 'value'))

        for block in self.blocks:
            key = block['key']
            if block.get('type') == 'media':
                self.fields[key] = MediaChoiceField(
                    label=block['label'],
                    help_text=block.get('help', 'Choose an image from the Media library.'),
                    initial=overrides.get(key) or None,
                )
                continue
            widget = forms.Textarea(attrs={'rows': 3}) if block.get('multiline') else forms.TextInput()
            self.fields[key] = forms.CharField(
                label=block['label'],
                required=False,
                widget=widget,
                help_text=block.get('help', ''),
                initial=overrides.get(key) or block['default'],
            )

    def clean(self):
        cleaned = super().clean()
        for key, value in list(cleaned.items()):
            if isinstance(value, str):
                # Browsers send \r\n for line breaks; store plain \n.
                cleaned[key] = value.replace('\r\n', '\n')
        return cleaned

    def save(self):
        for block in self.blocks:
            key = block['key']
            raw = self.cleaned_data.get(key)
            if block.get('type') == 'media':
                value = str(raw.pk) if raw else ''
            else:
                value = raw or ''
            if value == '' or value == block['default']:
                ContentBlock.objects.filter(page=self.page_slug, key=key).delete()
            else:
                ContentBlock.objects.update_or_create(
                    page=self.page_slug, key=key, defaults={'value': value},
                )


# --- Editable lists shown on the public pages ---

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'category', 'description', 'order']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
        help_texts = {
            'category': 'The sector. Services with the same sector text are grouped under one filter button.',
            'title': 'The service name shown on its card.',
        }


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'department', 'location', 'level', 'scope', 'requirements', 'is_active']
        widgets = {
            'scope': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {'is_active': 'Show on the Careers page'}
        help_texts = {'level': 'e.g. Senior • Market related / Based on experience'}


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer', 'order']
        widgets = {'answer': forms.Textarea(attrs={'rows': 5})}
        help_texts = {'order': 'Lower numbers appear first. Type [media:ID] in the answer to place a Media library image.'}


class DivisionForm(forms.ModelForm):
    media = MediaChoiceField(help_text="Optional image from the Media library, shown beside the division.")

    class Meta:
        model = Division
        fields = ['title', 'subtitle', 'description', 'bullets', 'stats', 'comparison', 'media', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
            'bullets': forms.Textarea(attrs={'rows': 4}),
            'stats': forms.Textarea(attrs={'rows': 3}),
            'comparison': forms.Textarea(attrs={'rows': 5}),
        }


# --- Public contact form ---

class ContactForm(forms.ModelForm):
    popia_consent = forms.BooleanField(
        required=True,
        error_messages={'required': 'Please accept the consent policy to send your message.'},
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message', 'popia_consent']


# --- Public job application form ---

class ApplicationForm(forms.ModelForm):
    popia_consent = forms.BooleanField(
        required=True,
        error_messages={'required': 'Please accept the agreement to submit your application.'},
    )

    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'cv', 'message', 'popia_consent']
