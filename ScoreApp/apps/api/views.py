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


def data_validator(entity, body):
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
        adding = data_validator(entidad, body)
        if if_exists(element, adding) == True:
            return JsonResponse({'error': 'This {} entity already exists'.format(entidad)}, status=409)
        if len(adding) != 0:
            try:
                adding = entities[element](**adding)
                adding.save()
                respuesta = adding.to_dict()
            except IntegrityError as e:
                return JsonResponse({'error': '{}'.format(e)})	
        else:
            message = 'In order to create {} entity, you must provide data for the following fields : {}'.format(entidad, fields[entidad])
            return JsonResponse({'message': message})

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
        body = data_validator(nombre_entidad, body)
        for key, value in body.items():
            en_detalle.__setattr__(key, value) 
        en_detalle.save()
        en_detalle = en_detalle.to_dict()
        return JsonResponse(en_detalle, status=204)
    if request.method == 'DELETE':
        en_detalle.delete()
        return HttpResponse(204)
	
