from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from ponder import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^',include('ponder.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^bug_fixes/', views.categorizations_by_bugFixID, name='id'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
