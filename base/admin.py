from django.contrib import admin

admin.AdminSite.site_header = 'Сайт ИМИ СВФУ'
admin.AdminSite.index_title = 'Администрирование'
admin.AdminSite.index_template = 'admin/base/index.html'
