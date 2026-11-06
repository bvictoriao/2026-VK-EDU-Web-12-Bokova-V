from django.test import SimpleTestCase
from django.urls import reverse


class QuestionPagesTests(SimpleTestCase):
    def test_new_questions_are_ordered_by_date_and_paginated(self):
        response = self.client.get(reverse('questions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['questions']), 20)
        dates = [obj['created_at'] for obj in response.context['questions']]
        self.assertEqual(dates, sorted(dates, reverse=True))
        self.assertContains(response, '?page=2')
        self.assertContains(response, 'aria-current="page"')

    def test_hot_questions_are_ordered_by_rating(self):
        response = self.client.get(reverse('questions:hot'))
        self.assertEqual(response.status_code, 200)
        scores = [obj['score'] for obj in response.context['questions']]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(response.context['page_obj'].paginator.per_page, 20)

    def test_tag_filters_questions_and_handles_an_empty_result(self):
        response = self.client.get(reverse('questions:tag', args=['django']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['questions'])
        self.assertTrue(all('django' in obj['tags'] for obj in response.context['questions']))
        empty = self.client.get(reverse('questions:tag', args=['unknown-tag']))
        self.assertEqual(empty.status_code, 200)
        self.assertContains(empty, 'Вопросов пока нет.')

    def test_question_35_has_paginated_answers(self):
        url = reverse('questions:question', args=[35])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question']['id'], 35)
        self.assertEqual(len(response.context['answers']), 30)
        second = self.client.get(url, {'page': 2})
        self.assertEqual(second.status_code, 200)
        self.assertEqual(len(second.context['answers']), 7)
        self.assertEqual(second.context['page_obj'].number, 2)
        self.assertContains(second, 'Текст ответа')

    def test_unknown_question_returns_404(self):
        response = self.client.get(reverse('questions:question', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_bad_page_parameters_never_break_the_views(self):
        urls = [
            reverse('questions:index'),
            reverse('questions:hot'),
            reverse('questions:tag', args=['django']),
            reverse('questions:question', args=[35]),
        ]
        for url in urls:
            for value in ('text', '-1', '999999'):
                with self.subTest(url=url, page=value):
                    response = self.client.get(url, {'page': value})
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.context['page_obj'].number, 1)

    def test_creation_form_is_available_by_named_route(self):
        response = self.client.get(reverse('questions:ask'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/ask.html')
