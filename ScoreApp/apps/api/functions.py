from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
import json
from .models import Profesor, Estudiante, Actividad, Area, Nota

entities = {'profesores': Profesor,
            'estudiantes': Estudiante, 'actividades': Actividad, 'areas': Area, 'notas': Nota}
persona = ['tipo_id', 'id', 'nombre', 'email', 'telefono']

def checking_relationships(entity):
    '''
    This function collects all the fields on the entity which are foreign keys	
    '''
    tipos_campo = [campo for campo in entity._meta.fields]
    uno_muchos = []
    for campo in tipos_campo:
        if campo.many_to_one is True:
            uno_muchos.append(campo.name)
    return uno_muchos

def checking_dictionaries_fk(campos, body):
    '''
    This function checks if the fields on the json input which match with fk fields has dictionaries as values
    '''
    print(campos)
    print(type(campos))
    for key, value in body.items():
            if key in campos:
                if isinstance(value, dict) != True:
                    return JsonResponse({'error': 'the field {} must have a dictionary as a value'.format(key)})
    return True


def data_in_dictio(entity, body):
    dictio = {}
    fields = [field.name for field in entity._meta.fields]
    for key, value in body.items():
        if key in fields:
            dictio[key] = value
    return dictio

def if_exists(entity, dictio):
    if entities[entity] == Estudiante or entities[entity] == Profesor:
        if entities[entity].objects.filter(pk=dictio['id']).exists() == True:
            return True
    elif entities[entity] == Area:
        if Area.objects.filter(nombre=dictio['nombre'], grado=dictio['grado']).exists() == True:
            return True
    elif entities[entity] == Actividad:
        if Actividad.objects.filter(tipo=dictio['tipo'], nombre=dictio['nombre'], grado=dictio['grado']).exists() is True:
            return True
    elif entities[entity] == Nota:
        if Nota.objects.filter(estudiante=dictio['estudiante'], actividad=dictio['actividad']).exists() is True:
            return True
    else:
        return False

def required_keys(entidad, metodo, dictio):
    ''' 
    This function checks if the required keys for creating an entity are present:
    '''
    if metodo == 'POST':
        fields = [field.name for field in entidad._meta.fields]
        for key in fields:
            if key not in dictio:
                return False
        return True
    elif metodo == 'PUT':
        if entidad == 'Profesor' or entidad == 'Estudiante 'and 'id' in dictio:
            return True
        elif entidad == 'Area' and 'nombre' in dictio and 'grado' in dictio:
            return True
        elif entidad == 'Actividad' and 'tipo' in dictio and 'nombre' in dictio and 'grado' in dictio:
            return True
        elif entidad == 'Nota' and 'estudiante' in dictio and 'actividad' in dictio:
            return True
        else:
            return False

