from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken

from news import views
from news.models import News
from rest_framework import status


# Create your tests here.

# 그러면 저희 simple jwt로 받아서 로그인 인증하는 방식을 저기 테스트에 입력으로 받아올 때에는 어떤 값으로 받아올까요?

class NewsTestClass(TestCase):
    # TestCase 를 상속 받은 클래스를 만들어 주고

    def test_news_list(self):
        # 'test_' 로 시작하는 클래스 매서드를 만들어준다.
        # python manage.py test 가 이제부터 이 메서드를 테스트로 인식함.

        for i in range(10):
            News.objects.create(
                title=f"title{i}",
                content=f"content{i}",
                link=f"https://www.naver.com/{i}",
            )
        response = self.client.get('/api/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_news_create(self):
        # 여기서, 뉴스 생성하기 요청을 보냈음.
        user = User.objects.create_user(username='test', password='test')
        refresh = RefreshToken.for_user(user)
        # integration test
        response = self.client.post('/api/news/',
                                    headers={"Authorization": f"Bearer {refresh.access_token}"},
                                    data={
                                        'title': 'test_title', 'content': 'test_content',
                                        'link': 'https://www.naver.com'})

        # 응답이 201로 잘 오는지 확인
        self.assertEqual(response.status_code, 201)

        # 실제로 데이터베이스에 잘 저장되었는지 확인하기
        news = News.objects.get(pk=response.data['id'])

        # 데이터베이스에서 가져온 제목과, 아까 생성하기 요청보낼때 보낸 제목이 같은지 확인
        self.assertEqual(news.title, 'test_title')

    def test_news_delete(self):
        # 장고가 다 갖춰줘서 test를 쉽게 할 수 있는건가요?
        # 다른 프레임워크로 개발하게 되면 테스트 테스트 모듈을 따로 만들어서 직접 작성해주는 걸까요?
        news = News.objects.create(title='title', content='content', link='https://www.naver.com')
        response = self.client.delete(f'/api/news/{news.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(News.objects.filter(id=news.id).exists())

    def test_news_create_unauthenticated(self):
        # 여기서, 뉴스 생성하기 요청을 보냈음. 유저 엑세스 토큰 없이
        # integration test
        response = self.client.post('/api/news/',
                                    data={
                                        'content': 'test_content', 'link': 'https://www.naver.com'})
        # 응답이 401로 잘 오는지 확인
        self.assertEqual(response.status_code, 401)

    def test_news_update(self):
        # 그러면 저 테스트를 위한 Model을 설계하고, delete를 수행하는 APIView를 작성해야 할거고 오
        news = News.objects.create(title='title', content='content', link='https://www.naver.com')
        response = self.client.put(f'/api/news/{news.id}', data={'title': 'updated_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(News.objects.get(id=news.id).title, 'updated_title')

    def test_news_create_bad_request(self):
        # 여기서, 뉴스 생성하기 요청을 보냈음. 타이틀 없이
        user = User.objects.create_user(username='test', password='test')
        refresh = RefreshToken.for_user(user)
        # integration test
        response = self.client.post('/api/news/',
                                    headers={"Authorization": f"Bearer {refresh.access_token}"},
                                    data={
                                        'content': 'test_content', 'link': 'https://www.naver.com'})

        # 응답이 400로 잘 오는지 확인
        self.assertEqual(response.status_code, 400)

    def test_rps_logic(self):
        # unit test
        self.assertEqual(views.rps_logic('paper', 'rock'), 'win')
        self.assertEqual(views.rps_logic('scissors', 'rock'), 'lose')
