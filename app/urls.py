from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from manager.views import EntryListView
from django.contrib.auth.decorators import login_required

from codeExtent import site_settings

admin.autodiscover()
admin.site.site_header = site_settings.SITE_NAME

urlpatterns = [
    url(r'^$', 'manager.views.entry_search', name='home'),
    url(r'^admin42/', admin.site.urls),
    url(r'^entry/', include('manager.urls.entry')),
    url(r'^category/', include('manager.urls.category')),
    url(r'^api/', include('api.urls')),

]
