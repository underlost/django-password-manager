from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    # url(r'^$', login_required(EntryListView.as_view()), name='details_entry'),
    url(r'^entries.json$', get_entries, name='api_get_entries'),
    # url(r'random_key.json$', 'api.views.get_random_key', name='api_get_entries'),
    url(r'search.json$', get_search, name='api_get_search'),
    url(r'entry/add$', post_entry_add, name='api_post_entry_add'),
]
