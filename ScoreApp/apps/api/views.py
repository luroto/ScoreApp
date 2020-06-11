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
fields = {'Profesor': persona, 'Estudiante': persona, 'Area': ['nombre', 'grado', 'profesor'], 'Actividad': [
    'tipo', 'nombre', 'descripcion', 'area', 'grado', 'fecha'], 'Nota': ['estudiante', 'actividad', 'nota']}


def data_in_dictio(entity, body):
    dictio = {}
    for key, value in body.items():
        if key in fields[entity]:
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
        for key in fields[entidad]:
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
    
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def get_all_elements(request):
    element = request.path.split('/')
    element = element[2]
    entidad = entities[element].__name__
    if request.method == 'GET':
        conjunto = entities[element].objects.values()
        lista = [entidad for entidad in conjunto]
        respuesta = {element: lista}
    elif request.method == 'POST':
        body = request.body.decode('utf-8')
        body = json.loads(body)
        # gets a dictio from the JSON dictionary
        adding = data_in_dictio(entidad, body)
        # Checks if the minimum requirements (dictionary keys)  are present
        if required_keys(entidad, request.method, body) is False:
            return JsonResponse({'error': 'In order to create this {} entity, you must provide he following fields in a JSON format {}'.format(entidad, fields[entidad])})	
        if if_exists(element, adding) == True:
            return JsonResponse({'error': 'This {} entity already exists'.format(entidad)}, status=409)
        try:
            creating = entities[element]()
            creating.save()
            respuesta = creating.to_dict()
            return JsonResponse(respuesta)
        except (IntegrityError, KeyError) as e:
            return JsonResponse({'error': '{}'.format(e)})	

    return JsonResponse(respuesta, status=201)


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def detailed_persona(request, documento):
    element = request.path.split('/')
    element = element[2]
    nombre_entidad = entities[element].__name__
    not_exist = {'error': "In {} this ID doesn't exist".format(element)}
    if element != 'notas':
        try:
            en_detalle = entities[element].objects.get(pk=documento)
        except ObjectDoesNotExist:
            return JsonResponse(not_exist, status=404)
    else:
        try:
            en_detalle = Nota.objects.get(nombre=documento)
        except ObjectDoesNotExist:
            return JsonResponse(not_exist, status=404)
    if request.method == 'GET':
        en_detalle = en_detalle.to_dict()
        return JsonResponse(en_detalle, status=200)
    if request.method == 'PUT':
        body = request.body.decode('UTF-8')
        body = json.loads(body)
        body = data_in_dictio(nombre_entidad, body)
        print(en_detalle)
        for key, value in body.items():
            en_detalle.__setattr__(key, value) 
        en_detalle.save()
        print(en_detalle)
        en_detalle = en_detalle.to_dict()
        return JsonResponse(en_detalle, status=204)
    if request.method == 'DELETE':
        en_detalle.delete()
        return HttpResponse(204)

@csrf_exempt
def all_students_per_course(request, curso):
    pass
