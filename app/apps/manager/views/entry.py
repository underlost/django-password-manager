from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import datetime
from django.shortcuts import redirect
from django.conf import settings
from manager.forms import EntryForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from manager.models import Entry, Category
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.http import HttpResponse

from manager.utils import AESCipher

class EntryDetailView(DetailView):
    """ Details about a given entry """
    model = Entry
    context_object_name = 'e'
    template_name = 'manager/entry_get.html'

    def get_context_data(self, **kwargs):
        engine = AESCipher(settings.MASTER_KEY)
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        decrypted = engine.decrypt(context['entry'].password)
        print(decrypted)
        context['decrypted_password'] = decrypted
        return context


class EntryListView(ListView):
    model = Entry
    context_object_name = 'entries'
    template_name = 'manager/entry_list.html'
    paginate_by = 200

    def get_queryset(self):
        return Entry.objects.public()

class EntryByCategoryListView(ListView):
    model = Entry
    context_object_name = 'entries'
    template_name='manager/entry_list.html'
    paginate_by = 200

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.pop('pk'))
        return Entry.objects.public().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(EntryByCategoryListView, self).get_context_data(**kwargs)
        context.update({'category' : self.category, })
        return context

class PersonalEntryListView(ListView):
    model = Entry
    context_object_name = 'entries'
    template_name = 'manager/entry_list.html'
    paginate_by = 200

    def get_queryset(self):
        u = self.request.user
        return Entry.objects.filter(user=u)

class EntryCreate(CreateView):
    """ Enables creation of new entries """

    model = Entry
    template_name = 'manager/entry_update.html'
    form_class = EntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create New Entry'
        context['updating'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry = form.save()
            messages.add_message(request, messages.INFO, u'New entry added: {}'.format(entry.title))
            return redirect('passe.manager:home')
        else:
            form = EntryForm()
            messages.add_message(request, messages.INFO, u'Unable to create new entry')
        return render(request, self.template_name, locals())


class EntryUpdate(UpdateView):
    """ Enables update of a given entry """
    model = Entry
    template_name = 'manager/entry_update.html'
    form_class = EntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Entry'
        context['updating'] = True
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EntryForm(request.POST, instance=self.object)
        if form.is_valid():
            entry = form.save()
            messages.add_message(request, messages.INFO, u'Entry updated: {}'.format(entry.title))
            return redirect('passe.manager:home')
        else:
            form = EntryForm(instance=self.object)
        return render(request, self.template_name, locals())


class EntryDelete(DeleteView):
    """ Enables deletion of a given entry """
    model = Entry
    context_object_name = 'obj'
    template_name = 'manager/delete.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.WARNING, "Entry deleted")
        return super(DeleteView, self).post(request, *args, **kwargs)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def entry_search(request):

    # Loads the categories
    categories = Category.objects.all()

    # Loads the entries
    if request.POST:
        if request.POST['search']:
            term = request.POST['search']
            entries = Entry.objects.public().filter(Q(title__icontains=term) | Q(comment__icontains=term))
            search = request.POST['search']
        else:
            entries = Entry.objects.public()

        if len(entries) == 0:
            messages.add_message(request, messages.WARNING, u'No entries related to {}'.format(request.POST['search']))
    else:
        entries = Entry.objects.public()

    return render(request, 'manager/entry_list.html', locals())
