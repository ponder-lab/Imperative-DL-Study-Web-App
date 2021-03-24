from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
#from ponder.views import CategorizationsListView,BugFixesListView, CategorizersListView, CommitDetailsListView, CommitsListView, DatasetsListView, ProblemCategoriesListView, ProblemCausesListView, ProblemFixesListView, ProblemSymptomsListView
app_name = 'ponder'

urlpatterns=[
    #url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    #path('categorizations/', views.CategorizationsListView.as_view(), name='categorizations_changelist'),
    path("commits", views.CommitsTableView.as_view(), name='commits_table'),
    path("commits/<str:pk>", views.CommitDetailsTableView.as_view(), name='commits_details'),
    path("bug_fixes/", views.BugFixesTableView.as_view(), name='bugfixes_table'),
    url('bug_fixes/<int:pk>', views.id, name='id'),
    path('categorizations/add', views.AddCategorization, name='categorizations_add'),
    url('categorizations', views.search, name='categorizations_filter'),
	path("success_categorization/<str:pk>", views.success_categorization, name='success_categorization'),
    path('create_prob_category/<str:pk>', views.ProblemCategoryCreateView.as_view(), name='create_problem_category'),
    path('create_prob_cause/<str:pk>', views.ProblemCauseCreateView.as_view(), name='create_problem_cause'),
    path('create_prob_symptom/<str:pk>', views.ProblemSymptomCreateView.as_view(), name='create_problem_symptom'),
    path('create_prob_fix/<str:pk>', views.ProblemFixCreateView.as_view(), name='create_problem_fix'),
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
