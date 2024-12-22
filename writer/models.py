from django.db import models
from account.models import CustomUser

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=20000)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False, verbose_name="Is this a premium article?")

    user = models.ForeignKey(CustomUser, max_length=25, on_delete=models.CASCADE, null=True)
