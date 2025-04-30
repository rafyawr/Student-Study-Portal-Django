from django.db import models
from django.contrib.auth.models import User

def get_default_user():
    return User.objects.get(username="rafayshahjehan").id 

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title



class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.title


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    due = models.DateField()
    is_finished = models.BooleanField(default=False)


    def __str__(self):
        return self.subject
    


