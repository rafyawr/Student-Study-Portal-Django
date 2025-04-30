from django.contrib import admin
from .models import ToDo, Notes, Homework


admin.site.register(ToDo)
admin.site.register(Notes)
admin.site.register(Homework) 
