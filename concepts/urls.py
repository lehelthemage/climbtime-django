from django.conf.urls import patterns, url

from concepts import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^conceptdetail/(?P<concept_id>\w+)/$', 'concepts.views.concept_detail', name='conceptdetail'),
                       url(r'^conceptupdate/(?P<concept_id>\w+)/$', 'concepts.views.concept_update', name='conceptupdate'),
                       url(r'^newcategory/', 'concepts.views.new_category', name='newcategory'),
                       url(r'^addcategory/', 'concepts.views.add_category', name='addcategory'),
                       url(r'^categorydetail/(?P<category_id>\w+)/$', 'concepts.views.category_detail', name='categorydetail'),
                       url(r'^categoryupdate/(?P<category_id>\w+)/$', 'concepts.views.category_update', name='categoryupdate'),
                       url(r'^parentautocomplete/', 'concepts.views.autocomplete_parents', name='parentautocomplete'),
                       url(r'^getcategoryproperties/$', 'concepts.views.get_category_properties', name='getcategoryproperties'),
                       url(r'^login/$', 'concepts.views.login_view', name='login'),
                       url(r'^logout/$', 'concepts.views.logout_view', name='logout'),
                       url(r'^authenticate/$', 'concepts.views.login', name='authenticate'),
                       url(r'^ajax_upload_media/$', 'concepts.views.ajax_upload_media', name='ajax_upload_media'),



)


