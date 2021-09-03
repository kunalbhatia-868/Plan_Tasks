from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from base import models

# Create your views here.


class TaskList(LoginRequiredMixin, ListView):
    model=models.Task
    template_name='base/task_list.html'
    context_object_name='task_list'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['task_list']=context['task_list'].filter(user=self.request.user)
        context['count']=context['task_list'].filter(complete=False).count()
        
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['task_list'] = context['task_list'].filter(
                title__startswith=search_input
            )

        context['search_input']=search_input

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model=models.Task
    template_name='base/task_detail.html'
    context_object_name='task'


class TaskCreate(LoginRequiredMixin,CreateView):
    model=models.Task
    template_name='base/task_create.html'    
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')


    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=models.Task
    template_name='base/task_create.html'
    fields = ['title', 'description', 'complete']
    success_url=reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=models.Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
