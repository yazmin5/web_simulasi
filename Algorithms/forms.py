from django.forms import ModelForm
from .models import Documents, DocumentsDDPR
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

# Form for Distance-Decay PageRank
class DocsFormsDDPR(ModelForm):
    class Meta:
        model = DocumentsDDPR
        fields = '__all__'