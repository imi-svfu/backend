from django.db.models import (Model, CharField, TextField, DateTimeField,
                              ForeignKey, SET_NULL)


class Page(Model):
    """
    Статические строницы
    """
    title = CharField('заголовок', max_length=100)
    markdown = TextField('текст в формате Markdown', blank=True, default='')
    created = DateTimeField('время создания')
    changed = DateTimeField('время изменения')
    author = ForeignKey('auth.User', on_delete=SET_NULL, verbose_name='автор',
                        blank=True, null=True)

    class Meta:
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'

    def __str__(self):
        return self.title
