from datetime import timedelta ,datetime,datetime
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from .validation import validate_author_email
from django.utils.timesince import timesince
# Create your models here.
PUBLISH_CHOICE=(('draft','Draft'),
                ('public','Public'),
                ('private','Private'))


class postmodel(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField (max_length=120,null=False, verbose_name="post title", unique=True)
    slug=models.SlugField(null=True, blank=True)
    context=models.TextField(null=True,blank=True)
    publish=models.CharField(max_length=120,choices=PUBLISH_CHOICE, default='draft')
    view_count=models.IntegerField(default=0)
    publish_date=models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    author_email=models.EmailField(max_length=120,validators=[validate_author_email], null=True, blank=True)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(postmodel,self).save(*args,**kwargs)    

    class Meta:
        verbose_name='Post'
        verbose_name_plural='Posts'

    def __str__(self):
        return self.title    
    @property
    def age(self):
       # if str(self.publish)=='Public':
            now=datetime.now()
            publish_time=datetime.combine(self.publish_date,
                                            datetime.now().min.time())
            try:
                difference=now-publish_time                                       
            except:
                return 'unknown'
            if (difference<=timedelta(minutes=1)):
                return 'just now'
            return '{time} ago'.format(time=timesince(publish_time).split(', ')[0])        
        #return "not published"    