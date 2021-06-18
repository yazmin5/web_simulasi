from django.forms import ModelForm
from .models import Documents
from .models import DocumentsPageRank

# Form for EpiRank
class DocsForms(ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'

# Form for PageRank
class DocsFormsPageRank(ModelForm):
    class Meta:
        model = DocumentsPageRank
        fields = '__all__'