from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
app_name = 'ponder'

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('commits/<str:pk>', views.CommitDetailsTableView.as_view(), name='commits_details'),
    url('commits', views.CommitsTableView, name='commits_table'),
    path('bug_fixes/', views.BugFixesTableView.as_view(), name='bugfixes_table'),
    url('bug_fixes/<int:pk>', views.categorizations_by_bugFixID, name='id'),
    path('categorizations/update_categorization', views.update_categorization, name='update_categorization'),
    path('categorizations/delete_categorization', views.delete_categorization, name='delete_categorization'),
    path('categorizations/new', views.AddCategorization, name='categorizations_add'),
    url('categorizations', views.categorizations_by_userID, name='categorizations_filter'),
    path('success_categorization/<str:pk>', views.success_categorization, name='success_categorization'),
    path('forbidden/', views.permission_denied, name='permission_denied'),
    path('categorizers/new', views.AddCategorizer, name='categorizers_add'),
]
