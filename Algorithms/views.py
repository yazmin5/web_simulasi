from django.shortcuts import render
import joblib

# Create your views here.
def landingPage(request):
   return render(request, 'landingPage.html')

def EpiRank(request):
   return render(request, 'EpiRank.html')

def predictEpiRank(request):
   if request.method == 'POST':
      temp={}
      temp['File_Berangkat']=request.POST.get('File_Berangkat')
      temp['File_Pulang']=request.POST.get('File_Pulang')
      temp['daytime']=request.POST.get('daytime')
      temp['damping']=request.POST.get('damping')

   return None

def resultEpiRank(request):
   epirank_algorithm = joblib.load('model/Epirank_model.pkl')

   if request.method == 'POST':
      temp={}
      temp['File_Berangkat']=request.POST.get('File_Berangkat')
      temp['File_Pulang']=request.POST.get('File_Pulang')
      temp['daytime']=request.POST.get('daytime')
      temp['damping']=request.POST.get('damping')

   File_Berangkat = temp['File_Berangkat']
   File_Pulang = temp['File_Pulang']
   daytime = temp['daytime']
   damping = temp['damping']

   ans = epirank_algorithm(File_Berangkat, File_Pulang, daytime, damping)

   return render(request, "result.html", {'ans': ans} )