from django.conf.urls import patterns, include, url
from bribe.views import moderator_view
from django.contrib.auth.views import login,logout
from django.views.generic.simple import redirect_to

#from django.views.generic import RedirectView
#from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url('^mhome/$', moderator_view, name = "moderator_view"),
    url(r'^accounts/login/$', login, {'template_name': 'registration/login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logged_out.html'}),
#    url(r'^accounts/profile/$', redirect_to, {'url': '/'}),
    # Examples:
    # url(r'^$', 'bribe.views.home', name='home'),
    # url(r'^bribe/', include('bribe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
