from django.shortcuts import render, redirect
from django.template import loader 
from .models import *
from .forms import DocsForms
from .Epirank import run_epiRank, make_DiGraph, get_exfac, htbreak
import pandas as pd    # input DataFrame

# Create your views here.
def landingPage(request):
   return render(request, 'landingPage.html')


# ------------------------------- Epirank -----------------------------
def EpiRank(request):
   form = DocsForms()
   if request.method == 'POST':
      form = DocsForms(request.POST, request.FILES, request.FILES)
      if form.is_valid():
         form.save()
         obj = Documents.object.get
         return redirect('DocsEpiRank')
   
   context = {'form':form}
   return render(request, 'EpiRank/Form.html', context)

def DocsEpiRank(request):
   documents = Documents.objects.all()
   context = {'documents':documents}
   return render(request, "EpiRank/Data.html", context)

def resultEpiRank(request, pk):
   document = Documents.objects.get(id=pk)
   depart_file = document.uploaded_file_berangkat
   come_back_file = document.uploaded_file_pulang

   depart = pd.read_csv(depart_file)
   come_back = pd.read_csv(come_back_file)
   
   epi_vals = run_epiRank(depart, come_back)
   gb1,bb = htbreak(epi_vals, 3)
   # pict1 = nx.draw(depart, with_labels = True)
   # pict2 = nx.draw(come_back, with_labels = True)
   
   context = {'document':document, 'epi_vals':epi_vals, 'gb1':gb1}
   return render(request, "EpiRank/result.html", context)