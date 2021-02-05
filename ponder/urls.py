from django.urls import path,include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	path('<str:username>/',views.index, name='index'),
	path('<str:c_id>/', views.commit, name='commit'),
    path('<str:c_id>/detail/', views.detail, name='detail'),
    path('<str:c_id>/categorization/', views.categorization, name='categorization'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/<str:login>', include('django.contrib.auth.urls')),
    path('accounts/logout/<str:logout>', include('django.contrib.auth.urls'))
    ]