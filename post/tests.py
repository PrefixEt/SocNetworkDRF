import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from user.models import User
from .models import Posts, Likes
from .serializers import PostSerializer, LikeSerializer



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
        testing_post = Posts.objects.get(id=post_id)
        post_response = PostSerializer(testing_post)
        self.assertEqual(response.data, post_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




class LikeTests(BaseViewTest):


    def test_like_unlike(self):
        like_tester= self.create_user(
            email='testliker@example.com',
            first_name='Liker',
             last_name='Likerston',
              password='1111'
              )
        login_token = self.login_a_user('testliker@example.com', '1111')
        
        self.client.force_authenticate(user=like_tester, token=login_token.data['token'])  

        post_response = self.client.post(
            reverse("post-create"),
            data=json.dumps({
                "title": 'LiketestPostTitle',
                "message": 'LikePostMessage'
                }),
             content_type="application/json"      
            )

        test_data = {'Like':{'user_id':like_tester.id,'post_id':post_response.data['id']}}
        post_id = post_response.data['id']
        like_response = self.client.post(reverse("post-like", args=[post_id]), data=json.dumps({}), content_type="application/json")
        self.assertEqual(like_response.data, test_data)
       
    
    def test_like_list(self):



        like_tester1= self.create_user(
            email='testliker1@example.com',
            first_name='Liker1',
             last_name='Likerston',
              password='1111'
              )
        
        like_tester2= self.create_user(
            email='testliker2@example.com',
            first_name='Liker2',
             last_name='Likerston',
              password='1111'
              )
            
        like_tester3= self.create_user(
            email='testliker3@example.com',
            first_name='Liker3',
             last_name='Likerston',
              password='1111'
              )
        login_token1 = self.login_a_user('testliker1@example.com', '1111')
        login_token2 = self.login_a_user('testliker2@example.com', '1111')
        login_token3 = self.login_a_user('testliker3@example.com', '1111')


        self.client.force_authenticate(user=like_tester1, token=login_token1.data['token'])  

        post_response = self.client.post(
            reverse("post-create"),
            data=json.dumps({
                "title": 'LiketestPostTitle',
                "message": 'LikePostMessage'
                }),
             content_type="application/json"      
            )

        post_id = post_response.data['id']

        like_response = self.client.post(reverse("post-like", args=[post_id]), data=json.dumps({}), content_type="application/json")

        self.client.force_authenticate(user=like_tester2, token=login_token2.data['token'])  
        like_response = self.client.post(reverse("post-like", args=[post_id]), data=json.dumps({}), content_type="application/json")

        self.client.force_authenticate(user=like_tester3, token=login_token3.data['token'])  
        like_response = self.client.post(reverse("post-like", args=[post_id]), data=json.dumps({}), content_type="application/json")
        
   
        test_data_obj = Likes.objects.filter(post_id=post_id)
        test_response = LikeSerializer(test_data_obj, many=True)
        response = response = self.client.get(reverse("post-like-list", args=[post_id]))
        self.assertEqual(response.data, test_response.data)



