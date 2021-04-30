from django.forms import ModelForm
from .models import Documents

class DocsForms(ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'