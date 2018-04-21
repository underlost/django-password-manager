from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
admin.site.site_header = settings.SITE_NAME

urlpatterns = [
    url(r'^admin42/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^', include('coreExtend.urls')),
    url(r'^', include('manager.urls')),
]
