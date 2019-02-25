from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.utils.datetime_safe import datetime
import time


class TodoListView(generic.ListView):
    template_name = 'todo/list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(done=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = True
        return context


class DoneListView(generic.ListView):
    template_name = 'todo/list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(done=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = False
        return context


class TodoDetailView(generic.DetailView):
    template_name = 'todo/detail.html'
    model = Todo
    context_object_name = 'todo'


class CalendarView(generic.View):
    def get(self, request):
        return render(request, 'todo/calendar.html', locals())


class IndexView(generic.View):
    def get(self, request):
        return redirect('todo:todo-list')


@login_required
def alt(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.done = not todo.done
    todo.save()
    return redirect('todo:todo-list') if todo.done else redirect('todo:done-list')


@login_required
def event(request):
    events = []
    fr = datetime.strptime(request.GET.get('start', ''), '%Y-%m-%d')
    to = datetime.strptime(request.GET.get('end', ''), '%Y-%m-%d')
    print(fr, to)
    for todo in Todo.objects.filter(deadline__range=[fr, to]):
        events.append({
            'title': todo.title,
            'start': todo.deadline.strftime('%Y-%m-%d'),
            'end': todo.deadline.strftime('%Y-%m-%d'),
            'color': '#eee' if todo.done else '#6cf',
            'textColor': '#999' if todo.done else '#000'
        })
    return HttpResponse(json.dumps(events))
