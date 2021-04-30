from django.shortcuts import render, redirect
from django.template import loader 
from .models import *
from .forms import DocsForms
from .Epirank import *

# Create your views here.
def landingPage(request):
   return render(request, 'landingPage.html')

def EpiRank(request):
   form = DocsForms()
   if request.method == 'POST':
      form = DocsForms(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('DocsEpiRank')
   
   context = {'form':form}
   return render(request, 'EpiRank.html', context)

def DocsEpiRank(request):
   documents = Documents.objects.all()
   context = {'documents':documents}
   return render(request, "DocsEpirank.html", context)

def resultEpiRank(request, pk):
   document = Documents.objects.get(id=pk)
   context = {'document':document}
   return render(request, "resultEpirank.html", context)