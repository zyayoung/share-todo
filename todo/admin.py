from django.contrib import admin
from .models import *
from django.shortcuts import redirect, get_object_or_404


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


admin.site.site_header = "Share Todo"
admin.site.site_title = "Todo"
admin.site.register(Todo, TodoAdmin)
