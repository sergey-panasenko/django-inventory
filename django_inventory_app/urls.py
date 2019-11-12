'''
inventory urls
'''
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    #path('pdf/', views.QRCodesPDFView.as_view(), name='qrcodes_pdf'),
    re_path(r'^(?P<code>[0-9a-f]{8})$',views.codeView.as_view(), name='code'),
]
