from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
# ===============VIEWS===================================


class CustomLogin(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')


class RegisterPage(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')

        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todoapp/tasklist.html'
    context_object_name = 'tasks'
    #this helps us by not typing objct_list in for loop
    #eg for task in object_list

 #the below part is to display content only to the user who created it and kwargs is like to take the argument value when passed to it
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(status=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'todoapp/taskdetail.html'
    context_object_name = 'task'
    #this helps us by not using object in for loop(basically looks for an object list)
    #and this is why the "task is not iterable error was coming as it works with only one element"
    #eg for tasks in object


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'todoapp/taskcreateform.html'
    fields = ['title', 'description', 'status']
    success_url = reverse_lazy('task-list')
#the below code block is used to override the form which was automatically provided to us
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'todoapp/taskcreateform.html'
    success_url = reverse_lazy('task-list')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    #by default the name is "object"
    template_name = 'todoapp/taskdeleteform.html'
    success_url = reverse_lazy('task-list')


