from django.shortcuts import render, redirect, get_object_or_404, resolve_url
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
    if request.GET.get('start') and request.GET.get('end'):
        fr = request.GET.get('start')
        if 'T' not in fr:
            fr += 'T0:0:0'
        fr = datetime.strptime(fr, '%Y-%m-%dT%H:%M:%S')
        to = request.GET.get('end')
        if 'T' not in to:
            to += 'T0:0:0'
        to = datetime.strptime(to, '%Y-%m-%dT%H:%M:%S')
        todos = Todo.objects.filter(deadline__range=[fr, to])
    else:
        todos = Todo.objects.all()
    for todo in todos:
        events.append({
            'title': todo.title,
            'start': todo.deadline.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': todo.deadline.strftime('%Y-%m-%dT%H:%M:%S'),
            'color': '#eee' if todo.done else '#6cf',
            'textColor': '#999' if todo.done else '#000',
            'url': resolve_url('todo:todo-detail', todo.pk),
            'detail': todo.detail,
        })
    return HttpResponse(json.dumps(events))
