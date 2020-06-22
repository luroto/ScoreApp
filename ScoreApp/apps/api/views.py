from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
import json
from .models import Profesor, Estudiante, Actividad, Area, Nota
from .functions import checking_relationships, checking_dictionaries_fk, data_in_dictio, if_exists, required_keys

entities = {'profesores': Profesor,
            'estudiantes': Estudiante, 'actividades': Actividad, 'areas': Area, 'notas': Nota}
persona = ['tipo_id', 'id', 'nombre', 'email', 'telefono']

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
        adding = data_in_dictio(entities[element], body)
        # Checks if the minimum requirements (dictionary keys)  are present
        if required_keys(entities[element], request.method, body) is False:
            fields = [field.name for field in entities[element]._meta.fields]
            return JsonResponse({'error': 'In order to create this {} entity, you must provide he following fields in a JSON format {}'.format(entidad, fields)})	
        if if_exists(element, adding) == True:
            return JsonResponse({'error': 'This {} entity already exists'.format(entidad)}, status=409)
    foraneos = checking_relationships(entities[element])
    if len(foraneos) == 0:
            try:
                creating = entities[element](**adding)
                creating.save()
                respuesta = creating.to_dict()
            except (IntegrityError, KeyError) as e:
                return JsonResponse({'error': '{}'.format(e)})	
    else:
        if checking_dictionaries_fk(foraneos, adding) is True:
            respuesta = {'mensaje': 'llegue aca en Post mama mandame plataa'}
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
        body = data_in_dictio(entities[element], body)
        print(en_detalle)
        for key, value in body.items():
            print('{}: {}'.format(key,value))
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
    estudiantes = Estudiante.objects.filter(grado=curso)
    estudiantes = [estudiante.to_dict() for estudiante in estudiantes]
    return JsonResponse({'estudiantes': estudiantes})
    
