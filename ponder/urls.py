from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from ponder.views import CategorizationsListView,BugFixesListView, CategorizersListView, CommitDetailsListView, CommitsListView, DatasetsListView, ProblemCategoriesListView, ProblemCausesListView, ProblemFixesListView, ProblemSymptomsListView
app_name = 'ponder'

urlpatterns=[
    #url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^categorizations/$',views.categorizations,name='categorizations'),
    # path("view_categorizations/", CategorizationsListView.as_view(), name='categorizations_table'),
    # path("view_bugfixes/", BugFixesListView.as_view(), name='bugfixes_table'),
    # path("view_categorizers/", CategorizersListView.as_view(), name='categorizers_table'),
    # path("view_commitdetails/", CommitDetailsListView.as_view(), name='commitdetails_table'),
    # path("view_commits/", CommitsListView.as_view(), name='commits_table'),
    # path("view_datasets/", DatasetsListView.as_view(), name='datasets_table'),
    # path("view_problemcategories/", ProblemCategoriesListView.as_view(), name='problemcategories_table'),
    # path("view_problemcauses/", ProblemCausesListView.as_view(), name='problemcauses_table'),
    # path("view_problemfixes/", ProblemFixesListView.as_view(), name='problemfixes_table'),
    # path("view_problemsymptoms/", ProblemSymptomsListView.as_view(), name='problemsymptoms_table')
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
