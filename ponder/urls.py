from django.urls import re_path, path

from . import views

app_name = 'ponder'

urlpatterns=[
    re_path(r'^$',views.index,name='index'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
    path('commits/<str:pk>', views.CommitDetailsTableView.as_view(), name='commits_details'),
    re_path('commits', views.CommitsTableView, name='commits_table'),
    path('bug_fixes/', views.BugFixesTableView.as_view(), name='bugfixes_table'),
    re_path('bug_fixes/<int:pk>', views.categorizations_by_bugFixID, name='id'),
    path('categorizations/update_categorization', views.update_categorization, name='update_categorization'),
    path('categorizations/delete_categorization', views.delete_categorization, name='delete_categorization'),
    path('categorizations/new', views.AddCategorization, name='categorizations_add'),
    re_path('categorizations', views.categorizations_by_userID, name='categorizations_filter'),
    path('success_categorization/<str:pk>', views.success_categorization, name='success_categorization'),
    path('forbidden/', views.permission_denied, name='permission_denied'),
    path('categorizers/new', views.AddCategorizer, name='categorizers_add'),
    path('register/', views.register, name='register'),
]