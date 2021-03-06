from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from manager.views import *

ENTRY_URLS = [
    url(r'^$', login_required(EntryListView.as_view()), name='details_entry'),
    url(r'^add/$', login_required(EntryCreate.as_view()), name='add_entry'),
    url(r'^update/(?P<pk>[\w-]+)/$', login_required(EntryUpdate.as_view()), name='update_entry'),
    url(r'^delete/(?P<pk>[\w-]+)/$', user_passes_test(lambda u: u.is_superuser)(login_required(EntryDelete.as_view())), name='delete_entry'),
    url(r'^(?P<pk>[\w-]+)/$', login_required(EntryDetailView.as_view()), name='details_entry'),
]

CATEGORY_URLS = [
    # url(r'^(?P<pk>\d+)$', login_required(CategoryDetailView.as_view()), name='details_category'),
    url(r'^add/$', login_required(CategoryCreate.as_view()), name='add_category'),
    url(r'^list/(?P<pk>[\w-]+)/$', login_required(EntryByCategoryListView.as_view()), name='entry_category_list'),
    url(r'^update/(?P<pk>[\w-]+)/$', login_required(CategoryUpdate.as_view()), name='update_category'),
    url(r'^delete/(?P<pk>[\w-]+)/$', login_required(CategoryDelete.as_view()), name='delete_category'),
]

app_name="passe.manager"
urlpatterns = [
    url(r'^$', entry_search, name='home'),
    url(r'^me/$', login_required(PersonalEntryListView.as_view()), name='personal_entry_list'),
    url(r'category/', include(CATEGORY_URLS)),
    url(r'entry/', include(ENTRY_URLS)),
]
