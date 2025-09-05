from django.db import models
from django.urls import reverse
class Book(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    author=models.CharField(max_length=120,blank=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    cover=models.ImageField(upload_to='covers/',blank=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created']
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('shop:book_detail', args=[self.slug])
image = models.ImageField(upload_to='books/', blank=True, null=True)
