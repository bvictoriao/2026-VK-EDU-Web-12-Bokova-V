from datetime import datetime, timedelta, timezone

from django.http import Http404
from django.shortcuts import render

from core.pagination import paginate


AUTHORS = ['Mr. Freeman', 'Dr. House', 'Dr. Pepper']
CREATED_AT = datetime(2026, 11, 6, 10, 30, tzinfo=timezone.utc)
QUESTION_EXAMPLES = [
    {
        'title': 'Как подключить Bootstrap локально?',
        'text': 'Как подключить стили Bootstrap к HTML-странице и в каком порядке подключать собственный CSS?',
        'tags': ['html', 'bootstrap'],
    },
    {
        'title': 'Как расположить две колонки на странице?',
        'text': 'Хочу разместить список вопросов слева, а популярные теги справа. Как использовать сетку Bootstrap?',
        'tags': ['css', 'bootstrap'],
    },
    {
        'title': 'Как передать данные из view в шаблон Django?',
        'text': 'Есть список словарей в Python. Как передать его в шаблон и вывести карточки с помощью цикла?',
        'tags': ['python', 'django'],
    },
]

ANSWER_LIST = [
    {
        'id': i,
        'text': f'Пример ответа {i}. Разделите задачу на небольшие шаги, проверьте настройки и сравните результат с примером из материалов курса.',
        'author': AUTHORS[(i - 1) % len(AUTHORS)],
        'created_at': CREATED_AT + timedelta(days=1, minutes=i),
        'score': 38 - i,
        'vote': ['none', 'like', 'dislike'][(i - 1) % 3],
        'is_correct': i == 1,
    }
    for i in range(1, 38)
]

QUESTION_LIST = []
for i in range(1, 66):
    example = QUESTION_EXAMPLES[(i - 1) % len(QUESTION_EXAMPLES)]
    QUESTION_LIST.append({
        'id': i,
        'title': example['title'] if i <= 3 else f"{example['title']} Пример {i}",
        'text': example['text'],
        'tags': example['tags'],
        'author': AUTHORS[(i - 1) % len(AUTHORS)],
        'created_at': CREATED_AT + timedelta(minutes=i),
        'score': (i * 7) % 101,
        'vote': ['none', 'like', 'dislike'][(i - 1) % 3],
        'answer_count': len(ANSWER_LIST),
    })


def index(request):
    objects = sorted(QUESTION_LIST, key=lambda obj: obj['created_at'], reverse=True)
    page_obj = paginate(objects, request, per_page=20)
    return render(request, 'questions/index.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,
    })


def hot(request):
    objects = sorted(QUESTION_LIST, key=lambda obj: obj['score'], reverse=True)
    page_obj = paginate(objects, request, per_page=20)
    return render(request, 'questions/hot.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,
    })


def tag(request, tag_name):
    objects = [obj for obj in QUESTION_LIST if tag_name in obj['tags']]
    objects.sort(key=lambda obj: obj['score'], reverse=True)
    page_obj = paginate(objects, request, per_page=20)
    return render(request, 'questions/tag.html', {
        'tag_name': tag_name,
        'questions': page_obj.object_list,
        'page_obj': page_obj,
    })


def question(request, question_id):
    obj = next((obj for obj in QUESTION_LIST if obj['id'] == question_id), None)
    if obj is None:
        raise Http404('Вопрос не найден')
    objects = sorted(
        ANSWER_LIST,
        key=lambda answer: (answer['score'], answer['created_at']),
        reverse=True,
    )
    page_obj = paginate(objects, request, per_page=30)
    return render(request, 'questions/question.html', {
        'question': obj,
        'answers': page_obj.object_list,
        'page_obj': page_obj,
    })


def ask(request):
    return render(request, 'questions/ask.html')
