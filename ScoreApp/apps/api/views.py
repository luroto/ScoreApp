from django.http import JsonResponse
from .models import Profesor, Estudiante


def get_all_personas(request):
	if 'profesores' in request.path:
		raton = Profesor.objects.values()
		lista = [profesor for profesor in raton]
		respuesta = {'profesores': lista}
	elif 'estudiantes' in request.path:
		estudiantes = Estudiante.objects.values()
		lista = [estudiante for estudiante in estudiantes]
		respuesta = {'estudiantes': lista}
	return JsonResponse(respuesta)

def detailed_persona(request, documento):
	if 'profesores' in request.path:
		persona = Profesor.objects.get(pk=documento)
	elif 'estudiantes' in request.path:
		persona = Estudiante.objects.get(pk=documento)
	print(type(persona))
	persona = persona.to_dict()
	return JsonResponse(persona, safe=False)
# Create your views here.
