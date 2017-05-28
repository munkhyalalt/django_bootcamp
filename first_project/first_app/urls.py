from django.conf.urls import url

from first_app import views

app_name = 'first_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^records$', views.web_records, name='web_records'),
    url(r'^help$', views.help_page, name='help'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
]
