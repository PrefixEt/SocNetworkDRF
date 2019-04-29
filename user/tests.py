import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import User
from .serializers import UserSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

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
        # add test data
        self.user = User.objects.create_superuser(            
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

        self.create_user(email='testM1@example.com',first_name='Garry', last_name='Garrison', password='1111')
        self.create_user(email='testM2@example.com',first_name='Jeff', last_name='Jeferson', password='2222')
        self.create_user(email='testM3@example.com',first_name='Bob', last_name='Robertson', password='3333')
        self.terk_terklton = self.create_user(email='testM4@example.com',first_name='Terk', last_name='Terklton', password='4444')
        



class GetAllUsersTest(BaseViewTest):

    def test_get_all_users(self):
        """
        This test ensures that all Users added in the setUp method
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("user-all")
        )
        # fetch the data from db
        expected = User.objects.all()
        serialized = UserSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetUserByIdTest(BaseViewTest):
    def test_get_user_by_id(self):
        user_id = self.terk_terklton.id
        user_response = self.client.get(reverse("user-by-id",  args=[user_id]))
        serialized_test_user = UserSerializer(self.terk_terklton)
        self.assertEqual(user_response.data, serialized_test_user.data)


class SignUpUserTest(BaseViewTest):
    def test_create(self):
        test_sign_up_data = {
            "email":"UnitTestUser@example.com",
            "first_name":"Mitchel",
            "last_name":"Mitchelson",
            "password":"asdfg",
            }
        email = test_sign_up_data['email']
        response = self.client.post(
            reverse('user-create'),
            data=json.dumps(test_sign_up_data),
            content_type="application/json" 
             )
        test_user = User.objects.get(email=email)
        serialize_test_data = UserSerializer(test_user)
        self.assertEqual(response.data, serialize_test_data.data)


class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
    
        response = self.login_a_user(email = "testM4@example.com", password= "4444")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)