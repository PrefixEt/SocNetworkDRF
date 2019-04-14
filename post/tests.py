import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from user.models import User
from .models import Posts
from .serializers import PostSerializer



class BaseViewTest(APITestCase):
    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = ''
       
        

    @staticmethod
    def create_user(*args, **kwargs):
        if kwargs['email'] and kwargs['first_name'] and kwargs['last_name'] and kwargs['password']:
            user = User.objects.create(
                email=kwargs['email'],
                first_name=kwargs['first_name'],
                last_name=kwargs['last_name'],
                password=kwargs['password']
                )
            return user
    
    
    def login_a_user(self, email="", password=""):
        url = reverse("auth-login")

        return self.client.post(
            url,
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )


    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(email='testpostuser@example.com',first_name='Poster', last_name='Posterson', password='1111')
        login = self.login_a_user('testpostuser@example.com','1111')
        self.token= login.data['token']



class GetAllPostsTest(BaseViewTest):

    def test_get_all_posts(self):
        """
        This test ensures that all Users added in the setUp method
        exist when we make a GET request to the user/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("posts-all")
        )
        # fetch the data from db
        expected = Posts.objects.all()
        serialized = PostSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePostTest(BaseViewTest):
    def test_create_post(self):
        
        url = reverse("post-create")
        self.client.force_authenticate(user=self.user, token=self.token)  
       
        response = self.client.post(
            url,
            data=json.dumps({
                "title": 'TestingPostTitle',
                "message": 'TestingPostMessage'
            }),
             content_type="application/json"           
            
        )
        post_id = response.data['id']
        post_response = self.client.get(reverse("post-by-id",  args=[post_id]))
        self.assertEqual(response.data, post_response.data)
        self.assertEqual(post_response.status_code, status.HTTP_200_OK)
