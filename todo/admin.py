from django.contrib import admin
from .models import *
from django.shortcuts import redirect, get_object_or_404
from django.utils.datetime_safe import datetime


class TodoAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('todo:todo-list')

    def response_change(self, request, obj):
        return redirect('todo:todo-detail', obj.pk)

    def delete_view(self, request, object_id, extra_context=None):
        get_object_or_404(Todo, id=object_id).delete()
        return redirect('todo:todo-list')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(TodoAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'deadline':
            if request.GET.get('date'):
                if 'T' in request.GET.get('date'):
                    t = datetime.strptime(request.GET.get('date'), "%Y-%m-%dT%H:%M:%S")
                    kwargs['initial'] = t
                else:
                    t = datetime.strptime(request.GET.get('date'), "%Y-%m-%d")
                    t = datetime.strptime(
                        '%d-%d-%dT23:59:59' % (t.year, t.month, t.day),
                        '%Y-%m-%dT%H:%M:%S'
                    )
            else:
                t = datetime.now()
                t = datetime.strptime(
                    '%d-%d-%dT23:59:59' % (t.year, t.month, t.day),
                    '%Y-%m-%dT%H:%M:%S'
                )
            kwargs['initial'] = t
        return super(TodoAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)


admin.site.site_header = "Share Todo"
admin.site.site_title = "Todo"
admin.site.register(Todo, TodoAdmin)
