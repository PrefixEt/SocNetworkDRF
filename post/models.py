from django.db import models
from user.models import User



class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    date_create = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True, auto_now_add=False)
    message = models.TextField(max_length=3000)
    likes = model.models.ManyToManyField(User)

    def __str__(self):
        return 'Message from <{}>[{}]: \n Title:{}'




