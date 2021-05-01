from django.shortcuts import render, redirect
from django.template import loader 
from .models import *
from .forms import DocsForms
import pandas as pd    # input DataFrame
import networkx as nx  # main data format
import numpy as np     # making matrix and multiplication
import csv
import copy

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

   def run_epiRank(g1, g2, d=0.95, daytime=0.5, number_of_loops=1000, exfac=None):
      graph_depart = make_DiGraph(g1, origin_col='origin', destination_col='destination', flow_col='flow', largest_connected_component=False, exclude_selfloop=False)
      graph_comeback = make_DiGraph(g2, origin_col='origin', destination_col='destination', flow_col='flow', largest_connected_component=False, exclude_selfloop=False)

      # g1 for department, g2 for coming back
      g1 = graph_depart
      g2 = graph_comeback
      ## exfac should be a matrix with the shape (N, 1)
      Ncount = g1.number_of_nodes() # both graph have same amount of nodes, so it's enough to count it just once

      ### prepare matrix ###
      print('start preparing matrices')

      # making adjacency matrix
      adj_matrix1 = nx.to_numpy_matrix(g1, weight = 'weight')
      adj_matrix2 = nx.to_numpy_matrix(g2, weight = 'weight')

      # transpose matrix adjacency
      adj_matrix1 = adj_matrix1.transpose()
      adj_matrix2 = adj_matrix2.transpose()

      # making weighted matrix for departing
      CN_D = adj_matrix1
      csum = CN_D.sum(axis=0) # count total per column
      CN = np.zeros((Ncount,Ncount)) # making new array with size NxN 
      for i in range(CN_D.shape[0]):
         for j in range(CN_D.shape[1]):
               s = float(csum[0,j])
               if s>0:
                  v = float(CN_D[i,j])
                  CN[i,j] = v/s

      # making weighted matrix for coming back
      CN_C = adj_matrix2
      csum2 = CN_C.sum(axis=0)
      CN2 = np.zeros((Ncount,Ncount))
      for i in range(CN_C.shape[0]):
         for j in range(CN_C.shape[1]):
               s = float(csum2[0,j])
               if s>0:
                  v = float(CN_C[i,j])
                  CN2[i,j] = v/s

      ### prepare external factor matrix if not specified ###
      # the same town should have same exfac values, meaning that town have same exfac values in both graph
      exfac_matrix = get_exfac(exfac, g1) # the exfac was defined as none at the beginning of this function

      ### initialize epidemic risk value matrix ###
      epidemic_risk = np.matrix(np.ones((1, Ncount))/float(Ncount)).transpose() ## init EpiRank values
      print('preparation done, start iterating')

      ### start running ###
      for i in range(number_of_loops):
         old_epidemic_risk = epidemic_risk.copy()
         epidemic_risk = (1. - d) * exfac_matrix + d * (daytime * CN2 * epidemic_risk + (1. - daytime) * CN * epidemic_risk)
         if np.ma.allequal(epidemic_risk, old_epidemic_risk): break

      #print('iteration count:', i)
      print('epirank calculation done after iteration: '+str(i))

      ### prepare result dic ###
      vals = [ i[0] for i in epidemic_risk.tolist() ]
      nodes = list(g1.nodes())
      epi_value = {}
      for i in range(len(epidemic_risk)):
         if i == 1:
               epi_value[nodes[2]] = vals[2]
         elif i == 2: 
               epi_value[nodes[1]] = vals[1]
         else: 
               epi_value[nodes[i]] = vals[i]

      gb1,bb = htbreak(epi_value, 3)

      return epi_value, gb1

   def make_DiGraph(df, origin_col='origin', destination_col='destination', flow_col='flow', largest_connected_component=True, exclude_selfloop=True):
      origins = df[origin_col].tolist()
      destinations = df[destination_col].tolist()
      flows = df[flow_col].tolist()
      g = nx.DiGraph()
      for o,d,f in zip(origins, destinations, flows):
         g.add_edge(o,d, weight=float(f))
      if largest_connected_component:
         g = max(nx.weakly_connected_component_subgraphs(g), key=len)
      if exclude_selfloop:
         g.remove_edges_from(g.selfloop_edges())
      print('graph construction done,'+' no. nodes: '+str( g.number_of_nodes()) +', no. edges: '+str(g.number_of_edges()))
      # edge_labels = nx.draw_networkx_edge_labels(g, pos=nx.spring_layout(g))
      return g

   def get_exfac(exfackey, g): # the inputs are exfac and a graph. the exfac values was defined at the beginnning of epirank function
      Ncount = g.number_of_nodes() #count number of codes in the graph
      if exfackey is None: # this part will only be run once at the beginning
         exfac = np.matrix(np.ones((1, Ncount))/float(Ncount)).transpose()
      elif isinstance(exfackey, dict): #isinstance() function returns True if the specified object is of the specified type(in this case dict), otherwise False
         ## please make sure all node is in dict ##
         exlist = []
         for n in g.nodes():
            if n in exfackey:
                  v = exfackey[n]
            else:
                  print('the dictionary do not contain info for node %s, set as 0'%(n))
                  v = 0
            exlist.append(v)
         exsum = float(sum(exlist))
         exlist2 = [ float(ex)/exsum for ex in exlist ]
         exfac = np.matrix(exlist2).transpose()
         #print exfac.shape
      elif isinstance(exfackey, str):
         ## please make sure all nodes have this attribute name ##
         exlist = []
         for n,v in g.nodes(data=True):
            if exfackey in v:
                  v2 = v[exfackey]
            else:
                  print('the node %s do not have the attribute %s, set as 0'%(n, exfackey))
                  v2 = 0
            exlist.append(v2)
         exsum = float(sum(exlist))
         exlist2 = [ float(ex)/exsum for ex in exlist ]
         exfac = np.matrix(exlist2).transpose()
      elif isinstance(exfackey, list):
         ## please make sure the list length match the number of nodes ##
         exlist = exfackey[:Ncount]
         exsum = float(sum(exlist))
         exlist2 = [ float(ex)/exsum for ex in exlist ]
         exfac = np.matrix(exlist2).transpose()
      elif isinstance(exfackey, np.matrix):
         ## please make sure the length of matrix has the same number as nodes ##
         if exfackey.shape==(Ncount, 1):
            exfac = exfackey
         elif exfackey.shape==(1, Ncount):
            exfac = exfackey.transpose()
         else:
            print('the shape is neither (%s, 1) nor (1, %s), force change to default exfac'%(str(Ncount), str(Ncount)))
            exfac = get_exfac(None, g)
      elif isinstance(exfackey, np.ndarray):
         exfackey = np.matrix(exfackey)
         if exfackey.shape==(Ncount, 1):
            exfac = exfackey
         elif exfackey.shape==(1, Ncount):
            exfac = exfackey.transpose()
         else:
            print('the shape is neither (%s, 1) nor (1, %s), force change to default exfac'%(str(Ncount), str(Ncount)))
            exfac = get_exfac(None, g)
      else:
         print('the input is not recognized, force back to default exfac')
         exfac = get_exfac(None, g)
      return exfac

   def htbreak(adic, g):
      alist = [ v for k,v in adic.items() ]
      temp = copy.copy(alist)
      breaks = []
      for i in range(g-1):
         avg = sum(temp) / float(len(temp))
         breaks.append(avg)
         temp2 = [ v for v in temp if v>avg ]
         temp = temp2
      #alist2 = []
      adic2 = {}
      for k,v in adic.items():
         lvl = None
         for i in range(len(breaks)):
               if v<=breaks[i]:
                  lvl = i
                  break
         if lvl is None:
               lvl = len(breaks)
         #alist2.append(lvl)
         adic2[k] = lvl

      return adic2, breaks

   depart = pd.read_csv(depart_file)
   come_back = pd.read_csv(come_back_file)
   
   epi_vals, gb1 = run_epiRank(depart, come_back)
   # pict1 = nx.draw(depart, with_labels = True)
   # pict2 = nx.draw(come_back, with_labels = True)
   
   context = {'document':document, 'epi_vals':epi_vals, 'gb1':gb1, 'pict1':pict1, 'pict2':pict2}
   return render(request, "EpiRank/result.html", context)