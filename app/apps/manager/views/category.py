from manager.models import Category
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from manager.forms import CategoryForm
from django.urls import reverse


class CategoryDetailView(DetailView):
    """ Details about a given entry """
    model = Category
    context_object_name = 'category'
    template_name = 'category_get.html'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 100


class CategoryCreate(CreateView):
    """ Enables creation of new entries """
    model = Category
    template_name = 'manager/category_update.html'
    form_class = CategoryForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create New Category'
        return context

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, "Category added")
        return super(CategoryCreate, self).post(request, *args, **kwargs)


class CategoryUpdate(UpdateView):
    """ Enables update of a given entry """
    model = Category
    template_name = 'manager/category_update.html'
    form_class = CategoryForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Category'
        context['updating'] = True
        return context

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, "Category updated")
        return super(CategoryUpdate, self).post(request, *args, **kwargs)


class CategoryDelete(DeleteView):
    """ Enables deletion of a given entry """
    model = Category
    context_object_name = 'obj'
    template_name = 'manager/delete.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.WARNING, "Category deleted")
        return super(CategoryDelete, self).post(request, *args, **kwargs)
