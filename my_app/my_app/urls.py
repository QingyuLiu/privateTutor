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
       url(r'^info_course/$', views.info_course),
       url(r'^profile_change_password$', views.profile_change_password, name='profile_change_password'),
       url(r'^profile_person_info$', views.profile_person_info, name='profile_person_info'),
       url(r'^page-blog-list$',views.homepage)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

