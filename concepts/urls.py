from django.conf.urls import patterns, url

from concepts import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^conceptdetail/(?P<concept_id>\w+)/$', 'concepts.views.conceptdetail', name='conceptdetail'),
                       url(r'^conceptupdate/(?P<concept_id>\w+)/$', 'concepts.views.conceptupdate', name='conceptupdate'),
)


