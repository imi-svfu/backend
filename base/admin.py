from datetime import datetime

from django.contrib import admin
from markdown import markdown

from .models import Page, Question

admin.AdminSite.site_header = 'Сайт ИМИ СВФУ'
admin.AdminSite.index_title = 'Администрирование'
admin.AdminSite.index_template = 'admin/base/index.html'
admin.AdminSite.enable_nav_sidebar = False


@admin.register(Page)
class AdminPage(admin.ModelAdmin):
    exclude = ['changed', 'created', 'author', 'html']

    def save_model(self, request, obj: Page, form, change):
        obj.html = markdown(obj.markdown)

        obj.changed = datetime.now()
        if not obj.created:
            obj.created = obj.changed

        if not obj.author:
            obj.author = request.user

        super().save_model(request, obj, form, change)


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
