from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
app_name = 'ponder'

urlpatterns=[
    url(r'^user_login/$',views.user_login,name='user_login'),
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
]
