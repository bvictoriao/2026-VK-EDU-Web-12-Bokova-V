from django.contrib.staticfiles import finders
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .pagination import paginate


class PaginationTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.objects = list(range(25))

    def test_second_page_contains_the_next_objects(self):
        page = paginate(self.objects, self.factory.get('/', {'page': '2'}))
        self.assertEqual(page.number, 2)
        self.assertEqual(list(page.object_list), list(range(10, 20)))
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_next())

    def test_invalid_page_falls_back_to_first_page(self):
        for value in ('text', '', '1.5', '0', '-1', '999999999999999999999999'):
            with self.subTest(page=value):
                page = paginate(self.objects, self.factory.get('/', {'page': value}))
                self.assertEqual(page.number, 1)
                self.assertEqual(list(page.object_list), list(range(10)))

    def test_missing_page_and_empty_list(self):
        request = self.factory.get('/')
        self.assertEqual(paginate(self.objects, request).number, 1)
        page = paginate([], request)
        self.assertEqual(page.number, 1)
        self.assertEqual(list(page.object_list), [])


class CorePagesTests(SimpleTestCase):
    def test_forms_render_with_shared_layout(self):
        for name in ('login', 'signup', 'profile'):
            with self.subTest(page=name):
                response = self.client.get(reverse(f'core:{name}'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f'core/{name}.html')
                self.assertTemplateUsed(response, 'core/layout/base.html')
                self.assertContains(response, reverse('questions:ask'))

    def test_profile_has_the_demo_user_block(self):
        response = self.client.get(reverse('core:profile'))
        self.assertContains(response, 'Аватар Dr. Pepper')
        self.assertContains(response, 'Выйти')

    def test_local_styles_and_images_are_discoverable(self):
        for name in ('css/bootstrap.min.css', 'css/style.css', 'img/avatar.svg', 'img/favicon.svg'):
            with self.subTest(asset=name):
                self.assertIsNotNone(finders.find(f'core/{name}'))
