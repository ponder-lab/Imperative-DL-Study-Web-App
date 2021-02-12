from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from ponder.views import CategorizationsListView,BugFixesListView
app_name = 'ponder'

urlpatterns=[
    #url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^categorizations/$',views.categorizations,name='categorizations'),
    path("view_categorizations/", CategorizationsListView.as_view(), name='categorizations_table'),
    path("view_bugfixes/", BugFixesListView.as_view(), name='bugfixes_table')
]

'''
urlpatterns = [
	path('<str:username>/',views.index, name='index'),
	path('<str:c_id>/', views.commit, name='commit'),
    path('<str:c_id>/detail/', views.detail, name='detail'),
    path('<str:c_id>/categorization/', views.categorization, name='categorization'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/<str:login>', include('django.contrib.auth.urls')),
    path('accounts/logout/<str:logout>', include('django.contrib.auth.urls'))
    ]
'''