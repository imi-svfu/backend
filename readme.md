# Бэкенд сайт ИМИ

Для API используется язык программирования Python, фреймворки Django и Django REST framework.

В Django созданы следующие приложения:

* `pages` — для публикации статических страниц.
* `questions` - для реализации функции вопросов и ответов.

При публикации на хостинге следует:

* создать файл настроек api/project/settings_production.py
* в файле настроек указать параметры:
  - `SECRET_KEY`
  - `DEBUG = False`
  - `ALLOWED_HOSTS`
  - `DATABASES`
  - `CSRF_COOKIE_SECURE = True`
  - `SESSION_COOKIE_SECURE = True`
* задать переменную окружения:

`export DJANGO_SETTINGS_MODULE="project.settings_production"`

Ссылки:

* [Развертывание на хостинге](https://docs.djangoproject.com/en/3.2/howto/deployment/)
* [Чеклист](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)
