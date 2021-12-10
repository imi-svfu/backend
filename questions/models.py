from django.db.models import (Model, BooleanField, CharField, TextField,
                              DateTimeField, ForeignKey, SET_NULL)


class Question(Model):
    """
    Вопрос и ответ модератора
    Вопрос задается пользователями. При создании вопроса он не виден обычным
    пользователям. Модераторы видят все вопросы и могут опубликовать вопрос со
    своим ответом.
    """
    title = CharField('заголовок', max_length=100)
    text = TextField('текст', blank=True, default='')
    posted = BooleanField('опубликован', default=False)
    answer = TextField('ответ', blank=True, default='')
    created = DateTimeField('время создания')
    changed = DateTimeField('время изменения')
    author = ForeignKey('auth.User', verbose_name='автор', on_delete=SET_NULL,
                        null=True)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.title
