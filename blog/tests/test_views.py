import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
print(now)


from django.test import TestCase, Client
from django.urls import reverse

class TestIndexView(TestCase):

    fixtures = ['/home/toshi/work/code_django/product_code/blog_apptest/fixture.json']

    def test_1(self):
        """一覧に記事が表示されていることを確認"""
        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(200, response.status_code)
        posts = response.context['blog_card']
        #記事が1件以上とれていること
        self.assertEqual(True, len(posts) > 0)


