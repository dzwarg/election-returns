from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^bystate/$', views.bystate, name='bystate'),
)
