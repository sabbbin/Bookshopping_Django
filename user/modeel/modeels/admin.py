from django.contrib import admin
from  .models import postmodel

class postmodeladmin(admin.ModelAdmin):
    fields=[
        'title',
        'slug',
        'context',
        'publish',
        'publish_date',
        'updated',
        'timestamp',
        'get_age'
    ]
    readonly_fields=['updated','timestamp','get_age']
    def get_age(self, obj,*args,**kwargs):
        return str(obj.age)
# Register your models here.

admin.site.register(postmodel,postmodeladmin)