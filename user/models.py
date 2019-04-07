from django.db import models


class User(models.Model):
    name = models.CharField(max_length=300)   
    description = models.TextField(max_length=3000)
    age = models.IntegerField()

    def __str__(self):
        return '<user: {}>'.format(self.name)

class Account(models.Model):
     email = models.EmailField(max_length=300)
     password_hash = models.CharField()
     date_registration = models.DateTimeField(auto_now=False, auto_now_add=True)
     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

