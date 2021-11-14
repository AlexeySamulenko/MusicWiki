from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .utils import *


class MusicHome(DataMixin, ListView):
    model = Music
    template_name = 'music/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main Page")
        return context | c_def

    def get_queryset(self):
        return Music.objects.filter(is_published=True).select_related('cat')


def about(request):
    return render(request, 'music/about.html', {'title': 'About Us'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'music/addpage.html'
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add News")
        return context | c_def

def contact(request):
    return HttpResponse("Contacts")


def login(request):
    return HttpResponse("Log In")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page Not Found</h1>')


class ShowPost(DataMixin, DetailView):
    model = Music
    template_name = 'music/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


class MusicCategory(DataMixin, ListView):
    model = Music
    template_name = 'music/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Music.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def
