from django.contrib import admin
from .models import Profesor, Estudiante, Area, Nota, Actividad

admin.site.register(Profesor)# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Area)
admin.site.register(Nota)
admin.site.register(Actividad)
