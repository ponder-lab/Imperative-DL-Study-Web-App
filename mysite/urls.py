from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path, path

from ponder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',views.index,name='index'),
    re_path(r'^special/',views.special,name='special'),
    re_path(r'^',include('ponder.urls')),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    re_path(r'^bug_fixes/', views.categorizations_by_bugFixID, name='id'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]