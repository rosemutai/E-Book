from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    pic = models.ImageField(blank=True, null=True, upload_to='book_image')

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

def create_user(sender, *args, **kwargs):
    if kwargs['created']:
        user = User.objects.create(username=kwargs['instance'],password="dummypass")


class Member(models.Model):
    member_id = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=10)
    branch = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=0)
    email=models.EmailField(unique=True)
    pic=models.ImageField(blank=True, upload_to='profile_image')

    def __str__(self):
        return str(self.member_id)


post_save.connect(create_user, sender=Member)


class Borrower(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.member.name+" borrowed "+self.book.title


class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete= models.CASCADE)

    def __str__(self):
        return self.user.username + " " + self.book.title

class Reviews(models.Model):
    review=models.CharField(max_length=100,default="none")
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    CHOICES = (
        ('0', '0'),
        ('.5', '.5'),
        ('1', '1'),
        ('1.5', '1.5'),
        ('2', '2'),
        ('2.5', '2.5'),
        ('3', '3'),
        ('3.5', '3.5'),
        ('4', '4'),
        ('4.5', '4.5'),
        ('5', '5'),
    )

    rating=models.CharField(max_length=3, choices=CHOICES, default='2')