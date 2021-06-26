from django.shortcuts import render, redirect
from django.template import loader 
from .models import *
from .forms import DocsForms
from .forms import DocsFormsPageRank
from .forms import DocsFormsDDPR
from .Epirank import run_epiRank, make_DiGraph, get_exfac, htbreak, draw_graph
from .PageRank import make_DiGraph, create_ODMatrix, run_Modified_PageRank, make_Dict, get_pearson_cor, htbreak, draw_spatial_graph_central_java, draw_spatial_graph_east_java, draw_spatial_graph_bali
from .DDPR import cre_DiGraph, draw_spatial_graph, run_ddpr, makeDict, pearsonCorr, htbreak, draw_spatial_graph
import pandas as pd
import numpy as np

def landingPage(request):
   return render(request, 'landingPage.html')

# ------------------------------- Epirank -----------------------------
def EpiRank(request):
   form = DocsForms()
   if request.method == 'POST':
      form = DocsForms(request.POST, request.FILES, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('DocsEpiRank')
   
   context = {'form':form}
   return render(request, 'EpiRank/Form.html', context)

def DocsEpiRank(request):
   documents = Documents.objects.all()
   documents = documents.order_by('-date_input')
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

   spatial_file = 'static/spatial file/Jabodetabek/BATASWILAYAH_JABODETABEK_250K.shp'
   od_file = depart_file
   pict1 = draw_graph(spatial_file, od_file)
   # pict2 = draw_graph(come_back)
   
   context = {'document':document, 'epi_vals':epi_vals, 'gb1':gb1, 'pict1':pict1}
   return render(request, "EpiRank/result.html", context)

# ------------------------------- PageRank -----------------------------
def PageRank(request):
   form = DocsFormsPageRank()
   if request.method == 'POST':
      form = DocsFormsPageRank(request.POST, request.FILES, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('DocsPageRank')

   context = {'form':form}
   return render(request, 'PageRank/Form.html', context)

def DocsPageRank(request):
   documents = DocumentsPageRank.objects.all()
   documents = documents.order_by('-Tanggal')
   context = {'documents':documents}
   return render(request, "PageRank/Data.html", context)

def resultPageRank(request, pk):
   document = DocumentsPageRank.objects.get(id=pk)
   wilayah = document.Wilayah
   file_Matriks_OD = document.File_Matriks_OD

   # Read the file which consists of a list of edges representing regions in East Java Province
   file_GDP = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'GDP Origin', 'GDP Destination'])
   file_MAN = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'MAN Origin', 'MAN Destination'])
   file_UNEM = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'UNEM Origin', 'UNEM Destination'])
   file_CRIM = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'CRIM Origin', 'CRIM Destination'])
   file_DENS = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'DENS Origin', 'DENS Destination'])
   file_LIT = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'LIT Origin', 'LIT Destination'])
   file_INF = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'INF Origin', 'INF Destination'])
   file_MIN = pd.read_excel(file_Matriks_OD, index_col=0, usecols=['ID', 'MIN Origin', 'MIN Destination'])

   file_Cases = document.File_Cases

   '''
   ATTENTION: files_csv and coeff MUST be in the same order
   '''

   files_csv = [file_LIT, file_CRIM, file_MAN, file_DENS, file_GDP, file_INF, file_UNEM, file_MIN]

   print(files_csv)

   OD_Matrix_List = [] # Prepare list to store the OD Matrix of each file

   coeff = [0.005888626148285406, 0.0404483855943423, 0.0983687893650872, 0.02609756597768234, 0.8263595276993987, -0.05640590716007701, 0.09487233256102165, -0.06171179914881331]

   # Read files, create graph for each, and construct OD Matrix
   for file in files_csv:

      print("File")
      print(file)

      # Assign value to other variables
      df_graph = file

      # Rename data frame columns' name
      df_graph.columns = ['Origin', 'Destination']

      print("DF_Graph")
      print(df_graph)

      df_graph = df_graph[df_graph['Origin'].notna()]

      # Create graph
      graph = make_DiGraph(df_graph, origin_col = 'Origin', destination_col = 'Destination')

      # Create list of OD Matrix
      OD_Matrix_List.append(create_ODMatrix(graph))

      print(OD_Matrix_List)

   # Calculate scores
   final_ranks = run_Modified_PageRank(graph, OD_Matrix_List, coeff)
   
   # Read the file which consists of number of Covid-19 cases in East Java Province by regions
   df_cases = pd.read_csv(file_Cases, index_col = 0)

   # Convert data frame to dictionary format
   cases = make_Dict(df_cases)

   # Calculate score
   corr_coeff = get_pearson_cor(final_ranks, cases[0])

   # Perform Head-Tails Breaks
   htdict, thres = htbreak(final_ranks, 3)

   htdict_replace = {2: 'Risiko Tinggi', 1:'Risiko Sedang', 0:'Risiko Rendah'}
   for x, y in htdict.items():
      htdict[x] = htdict_replace[y]

   index_list = list(range(1, len(final_ranks) + 1))

   for k, v in final_ranks.items():
            final_ranks[k] = round(v, 3)

   if wilayah == 'Jawa Timur':
      od_file = 'static/documents/source/Jawa Timur - OD_Matriks.csv'
      spatial_file = 'static/spatial file/Jawa Timur/RBI250K_BATAS_WILAYAH_AR.shp'

      pict = draw_spatial_graph_east_java(spatial_file, od_file, final_ranks, thres)

   if wilayah == 'Jawa Tengah':
      od_file = 'static/documents/source/Jawa Tengah - OD_Matriks.csv'
      spatial_file = 'static/spatial file/Jawa Tengah/RBI250K_BATAS_WILAYAH_AR.shp'

      pict = draw_spatial_graph_central_java(spatial_file, od_file, final_ranks, thres)
   
   if wilayah == 'Bali':
      od_file = 'static/documents/source/Bali - OD_Matriks.csv.csv'
      spatial_file = 'static/spatial file/Bali/RBI250K_BATAS_WILAYAH_AR.shp'

      pict = draw_spatial_graph_bali(spatial_file, od_file, final_ranks, thres)
   
   thres_round = list(np.around(np.array(thres), 2))
   thres_upper = thres_round[1]
   thres_lower = thres_round[0]

   context = {'document':document, 'final_ranks':final_ranks, 'corr_coeff':corr_coeff, 'htdict':htdict, 'thres':thres, 'index_list':index_list, 'pict':pict, 'thres_upper':thres_upper, 'thres_lower':thres_lower}
   return render(request, "PageRank/result.html", context)

# ------------------------------- Distance Decay PageRank -----------------------------

def DDPR(request):
   form = DocsFormsDDPR()
   if request.method == 'POST':
      form = DocsFormsDDPR(request.POST, request.FILES, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('DocsDDPR')
   
   context = {'form':form}
   return render(request, 'DDPR/Form.html', context)


def DocsDDPR(request):
   documents = DocumentsDDPR.objects.all()
   documents = documents.order_by('-Tanggal')
   context = {'documents':documents}
   return render(request, "DDPR/Data.html", context)


def resultDDPR(request, pk):
   document = DocumentsDDPR.objects.get(id=pk)
   file_Kasus = document.File_Kasus_Stasiun
   file_Jarak = document.File_Jarak

   #reading a file of COVID-19 cases and make it to dictionary
   df_case = pd.read_csv(file_Kasus, index_col = 0)
   case = makeDict(df_case, 'Nama', 'cases')

   #print(case)

   #reading OD matrix and making graph from it
   Matrix = pd.read_csv(file_Jarak)
   graph = cre_DiGraph(Matrix)

   #running the DDPR
   score = run_ddpr(graph)

   skor = score[0]

   #calculating the correlation coeff of score and cases
   corr = pearsonCorr(score[0],case)
   corr = round(corr, 3)

   score = score[0]

   print(score)
   # Perform Head-Tails Breaks
   risk1, thres1 = htbreak(skor, 3)

   risk_replace = {2: 'Risiko Tinggi', 1:'Risiko Sedang', 0:'Risiko Rendah'}
   for x, y in risk1.items():
      risk1[x] = risk_replace[y]

   index = list(range(1, len(skor) + 1))

   od = 'static/documents/OD Matrix 83,25 KM.csv'
   spatial_file = 'static/spatial file/Jawa Timur/jatim-kereta.shp'
   coordinate = 'static/spatial file/Jawa Timur/titik kereta.shp'

   gambar = draw_spatial_graph(spatial_file, od, skor, thres1, coordinate, df_case)

   df_score = pd.DataFrame(skor.items(), columns = ['Nama', 'Skor'])
   df_risk = pd.DataFrame(risk1.items(), columns = ['Nama', 'label'])

   df_merge = pd.merge(df_score, df_risk, on='Nama')
   df_merge['Skor'] = df_merge['Skor'].round(3)
   df_merge= df_merge.sort_values(by=['Skor'], ascending= False)

   dict_score = makeDict(df_merge, 'Nama', 'Skor')
   dict_risk = makeDict(df_merge, 'Nama', 'label')


   #print(dict_risk)
   
   context = {'document':document, 'score':score, 'risk':risk1, 'corr':corr, 'index':index, 'dict_score':dict_score, 'dict_risk':dict_risk, 'skor':skor, 'gambar':gambar}
   return render(request, "DDPR/result.html", context)