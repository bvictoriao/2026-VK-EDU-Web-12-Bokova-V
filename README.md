# 2026-VK-EDU-Web-12-Bokova-V

Учебный проект курса веб-разработки VK Education.

ДЗ1: статическая вёрстка сервиса вопросов и ответов на HTML, CSS и Bootstrap.
ДЗ2: Django views, маршруты, шаблоны и пагинация на данных-заглушках.

## Как открыть вёрстку ДЗ1

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

## Структура ДЗ1

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

## Страницы Django — ДЗ2

| URL | Страница |
| --- | --- |
| `/` | Новые вопросы |
| `/hot/` | Популярные вопросы |
| `/tag/django/` | Вопросы по тегу |
| `/question/35/` | Вопрос и ответы |
| `/ask/` | Создание вопроса |
| `/login/` | Вход |
| `/signup/` | Регистрация |
| `/profile/` | Настройки профиля |

`application/` — настройки проекта, `core/` — страницы пользователя, общий
каркас и пагинация, `questions/` — страницы вопросов. Пример семинара:
[Infinity10K/2026-fall-VK-EDU-Web](https://github.com/Infinity10K/2026-fall-VK-EDU-Web),
коммит `4b49674`.

Вопросы и ответы подготовлены в Python как списки словарей. Формы,
голосование и состояние авторизации пока демонстрационные. Пагинация работает
через `?page=2`; некорректные номера возвращают первую страницу.

## Локальный запуск Django

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Откройте http://127.0.0.1:8000/.

Настройки для локальной разработки заданы по умолчанию. Чтобы переопределить
их через окружение, скопируйте `.env.example` в `.env`, задайте свои значения и загрузите перед запуском:

```bash
cp .env.example .env
set -a
source .env
set +a
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

Откройте http://127.0.0.1:8000/. Нужен запущенный Docker Engine.
Compose автоматически читает `.env`, если файл существует; без него
используются настройки локальной разработки.

Код подключён через volume, `media/` хранится в отдельном именованном volume.
Если порт 8000 занят локальным сервером, остановите его перед запуском контейнера.

Для создания служебных таблиц Django при первом запуске:

```bash
docker compose exec web python manage.py migrate
```

## Проверка

```bash
python manage.py check
python manage.py test
```
