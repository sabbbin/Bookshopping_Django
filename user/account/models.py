from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser)
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class  MyUserManager(BaseUserManager):
    def create_user(self,  username,email, password=None):

        if not email:
            raise ValueError('user mus have an email address')

        user=self.model(
            username=  username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email,password):
        user=self.create_user(
            username,
            email,
            password=password,
        )

        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user

USERNAME_REGEX='^[a-zA-Z0-9.@+-]*$'

class MyUser(AbstractBaseUser):
    username=models.CharField(max_length=120,unique=True)
    firstname=models.CharField(max_length=120, default='sabin11224231231')
    lastname=models.CharField(max_length=120,default='sabin')
    rollno=models.IntegerField(null=True, default=0)
    #department=models.ForeignKey(departments,on_delete=models.CASCADE)
    #course=models.ManyToManyField(courses)
    email=models.EmailField()
    grade=models.IntegerField(null=True, default=0)
    image=models.FileField(upload_to='books',blank=True)
    password=models.CharField(max_length=120,default='sabin')
    
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    objects= MyUserManager()
    
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "does the user have a seficic permsion?"
        return True
    def has_module_perms(self,app_label):
        return True        



'''class profile(models.Model):
    profile=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    city=models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.user.username)

    def __unicode__(self):
        return str(self.user.username)

def post_save_model(sender, instance,created, *args, **kwargs):
    if created:
        try:
            profile.objects.create(user=instance)
        except:
            pass    

post_save.connect(post_save_model, sender=settings.AUTH_USER_MODEL)

'''




CHOICE=(('computer','computer'),
        ('civil','civil'),
        ('electrical','electrical'))
# Create your models here.


class departments(models.Model):
    Department=models.CharField(max_length=120)

class courses(models.Model):
    Course=models.OneToOneField(departments, on_delete=models.CASCADE)
    price=models.IntegerField()    


    


class teacher (models.Model):
    firstname=models.CharField(max_length=120)
    lastname=models.CharField(max_length=120)
    username=models.CharField(max_length=120)
    department=models.ForeignKey(departments,on_delete=models.CASCADE)
    course=models.OneToOneField(courses, on_delete=models.CASCADE)



class book (models.Model):
    
    title=models.CharField(max_length=120)
    uploaded_by=models.CharField(max_length=120)
    dateofpublish=models.DateField()
    content=models.TextField()
    slug=models.SlugField(unique=True)
    author=models.CharField(max_length=120)
    published_by=models.CharField(max_length=120)
  
    image=models.ImageField(upload_to='books',blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
        
    def __str__(self):
        return str(self.title)

    

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={'slug':self.slug})
    
    def get_remove_from_cart(self):
        return reverse("removetocart", kwargs={'slug':self.slug})     

    def get_add_to_cart(self):
        return reverse("addtocart", kwargs={'slug':self.slug})     


class history(models.Model):
    user=models.CharField(max_length=30)
    book=models.CharField(max_length=30)
    quantity=models.IntegerField(default=0)
    Price=models.PositiveIntegerField(default=0)
    totalprice=models.PositiveIntegerField(default=0)
   
    image=models.ImageField(upload_to='books',blank=True)

    def __str__(self):
        return str(self.user)


class orderbook(models.Model): 
    
    book=models.ForeignKey(book,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    Price=models.PositiveIntegerField(default=0)
    totalprice=models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.book.title)

class order(models.Model):
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    books=models.ManyToManyField (orderbook)
    start_date=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(unique=True)
    sum=models.PositiveIntegerField(default=0,blank=True)
  

   

    def slugg(self):
        return slugify(self.user)


    def __str__(self):
        return self.user.username   

    