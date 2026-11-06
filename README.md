# 2026-VK-EDU-Web-12-Bokova-V

Учебный проект курса веб-разработки VK Education.

ДЗ1: статическая вёрстка сервиса вопросов и ответов на HTML, CSS и Bootstrap.

## Как открыть

Откройте `public/index.html`.

## Страницы

| Файл | Содержимое |
| --- | --- |
| [base.html](public/base.html) | Общий каркас: шапка, две колонки, подвал |
| [index.html](public/index.html) | Список вопросов, три состояния голосования, пагинация |
| [question.html](public/question.html) | Вопрос, ответы, отметка правильного ответа, форма ответа |
| [ask.html](public/ask.html) | Форма создания вопроса |
| [login.html](public/login.html) | Форма входа |
| [signup.html](public/signup.html) | Форма регистрации и выбор аватарки |
| [profile.html](public/profile.html) | Настройки email, никнейма и аватарки |



## Структура

```text
public/
  base.html
  index.html
  question.html
  ask.html
  login.html
  signup.html
  profile.html
  static/
    css/    # Bootstrap 5.3.8 и собственный style.css
    js/     # папка для скриптов, пока не используются
    img/    # локальные аватарка и favicon
```

## Локальный запуск Django

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Откройте http://127.0.0.1:8000/.

Настройки для локальной разработки заданы по умолчанию. Чтобы переопределить
их через окружение, скопируйте `.env.example` в `.env` и загрузите перед запуском:

```bash
set -a
source .env
set +a
```
