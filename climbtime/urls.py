from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'', include('concepts.urls', namespace='concepts')),
    url(r'^concepts/', include('concepts.urls', namespace='concepts')),
    url(r'auth/', include('social_auth.urls')),

    #url(r'^accounts/', include('regme.urls')),
    #(r'^facebook/', include('django_facebook.urls')),
    #(r'^accounts/', include('django_facebook.auth_urls')),
    #url(r'^', include('mongo_auth.contrib.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
