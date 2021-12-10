from datetime import datetime

from django.contrib import admin

from .models import Question


@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    exclude = ['changed', 'created', 'author']

    def save_model(self, request, obj: Question, form, change):
        obj.changed = datetime.now()
        if not obj.created:
            obj.created = obj.changed

        if not obj.author:
            obj.author = request.user

        super().save_model(request, obj, form, change)
