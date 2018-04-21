from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()
admin.site.site_header = settings.SITE_NAME

urlpatterns = [
    url(r'^admin42/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^', include('coreExtend.urls')),
    url(r'^', include('manager.urls')),

    # Static
    url(r'^404/$', TemplateView.as_view(template_name="404.html"), name="404_page"),
    url(r'^500/$', TemplateView.as_view(template_name="500.html"), name="500_page"),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(template_name="humans.txt", content_type='text/plain')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
