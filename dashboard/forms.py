from django import forms
from .models import Record
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Explicit Save Button styled with Bootstrap
        self.helper.add_input(Submit('submit', 'Save Record', css_class='btn btn-success w-100 mt-3'))