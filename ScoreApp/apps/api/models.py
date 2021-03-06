#!/usr/bin/python3
'''
This file handles the Database tables and its fields.
'''
from django.db import models

documentos = [('CC', 'Cédula de ciudadania'),
               ('CE', 'Cédula de extranjería'), ('PA', 'Pasaporte')]

actividades = [('ENSAYO', 'Ensayo'), ('QUIZ', 'Quiz'),
                ('EXAMEN', 'Examen'), ('TALLER', 'Taller')]


class Persona(models.Model):
    '''
    Considering that profesores as estudiantes are personas, sharing common attributes, I created an abstract class, Personas
    '''
    tipo_id = models.CharField(max_length=10, choices=documentos)
    id = models.IntegerField(primary_key=True, default="")
    nombre = models.CharField("APELLIDOS Y NOMBRES", max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=10)

    def to_dict(self):
        ''' For creating a dictionary with all the object's attributes'''

        dictio = {}
        for key, value in self.__dict__.items():
            if key != '_state':
                dictio[key] = value
        return dictio

    def __str__(self):
        return "[{}] ({}, {}) {}".format(type(self).__name__, self.tipo_id, self.id, self.to_dict())

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True
        ordering = ['nombre']

        
class Profesor(Persona):

    class Meta:
        verbose_name_plural = 'Profesores'
    
class Estudiante(Persona):
    acudiente = models.CharField('APELLIDOS Y NOMBRES DEL ACUDIENTE', max_length=50, default='ACUDIENTE')
    grado = models.IntegerField('Grado y grupo del estudiante')

    class Meta:
        verbose_name_plural = 'Estudiantes'
    
class Area(models.Model):
    nombre = models.CharField("NOMBRE DEL AREA", max_length=10)
    grado = models.IntegerField()
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)

    class Meta:
        ordering = ['grado']

    def __str__(self):
        return '[{}] ({}, {}) {} '.format(type(self).__name__, self.grado, self.nombre, self.profesor)

        
class Actividad(models.Model):
    tipo = models.CharField(max_length=10, choices=actividades)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    grado = models.IntegerField()
    fecha = models.DateField()

    class Meta:
        verbose_name_plural = 'Actividades'
        ordering = ['grado']

    def __str__(self):
        return "[{}] ({}, {}) {}".format(type(self).__name__, self.grado, self.area, {'tipo': self.tipo, 'nombre': self.nombre, 'descripcion': self.descripcion, 'fecha': self.fecha})

        
class Nota(models.Model):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)
    nota = models.FloatField()

    class Meta:
        ordering = ['estudiante']

    def __str__(self):
        return "[{}] ({}) {}".format(type(self).__name__, self.actividad, {'estudiante': self.estudiante, 'nota': self.nota})
