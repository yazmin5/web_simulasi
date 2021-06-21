"""web_simulasi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Algorithms import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingPage, name="home"),

    path('EpiRank', views.EpiRank, name="EpiRank"),
    path('DocsEpiRank', views.DocsEpiRank, name="DocsEpiRank" ),
    path('resultEpiRank/<str:pk>/', views.resultEpiRank, name="resultEpiRank"),

    path('PageRank', views.PageRank, name="PageRank"),
    path('DocsPageRank', views.DocsPageRank, name="DocsPageRank" ),
    path('resultPageRank/<str:pk>/', views.resultPageRank, name="resultPageRank"),

    path('DDPR', views.DDPR, name="DDPR"),
    path('DocsDDPR', views.DocsDDPR, name="DocsDDPR" ),
    path('resultDDPR/<str:pk>/', views.resultDDPR, name="resultDDPR")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
