'''
inventory urls
'''
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('pdf/', views.QRCodesPDFView.as_view(), name='qrcodes_pdf'),
]
