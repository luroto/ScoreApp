from django.urls import path
from . import views

urlpatterns = [
	path('profesores', views.get_all_personas),
	path('estudiantes', views.get_all_personas),
	path('profesores/<int:documento>', views.detailed_persona),
	path('estudiantes/<int:documento>', views.detailed_persona),
]
