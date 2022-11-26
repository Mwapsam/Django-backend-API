from django.db import models
from authentication.models import User

# Create your models here.
class People(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    title = models.CharField(max_length=20, null=False, blank=False)
    food = models.CharField(max_length=20, null=False, blank=False)
    hobby = models.CharField(max_length=20, null=False, blank=False)
    location = models.CharField(max_length=20, null=False, blank=False)
    image = models.ImageField(upload_to="uploads/images/")
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.title