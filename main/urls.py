# main/urls.py
from django.urls import path # type: ignore
from .views import index, info_page, info_api

urlpatterns = [
    path('', index, name='index'),              # root -> index.html (opsional)
    path('api/info/', info_page, name='info_page'),      # HTML page
    path('api/info/json/', info_api, name='info_json'),  # JSON (opsional)
]
