from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('authorize/', views.Authorize.as_view(), name='authorize'),
    path('verify/<uuid:code>/', views.Verify.as_view(), name='verify'),
]