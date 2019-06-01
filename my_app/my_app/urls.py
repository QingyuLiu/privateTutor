"""my_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('account_app/', include('account_app.urls'))
"""
from django.conf.urls import url
from account_app import views
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin

urlpatterns = [
       url('admin/', admin.site.urls),
       url(r'^$', views.protect1),
       url(r'^register$', views.register),
       url(r'^login$', views.login),
       url(r'^login_validate$', views.login_validate),
       url(r'^me$', views.me),
       url(r'^logout$', views.logout),
       url(r'^info_course/$',views.info_course),
       url(r'^profile_change_password$',views.profile_change_password),
       url(r'^profile_person_info$',views.profile_person_info),
       url(r'^page-blog-list$',views.homepage)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

