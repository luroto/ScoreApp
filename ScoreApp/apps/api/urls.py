from django.urls import path
from . import views

urlpatterns = [
	path('profesores', views.get_all_elements),
	path('estudiantes', views.get_all_elements),
	path('actividades', views.get_all_elements),
	path('areas', views.get_all_elements),
	path('notas', views.get_all_elements),
	path('profesores/<int:documento>', views.detailed_persona),
	path('estudiantes/<int:documento>', views.detailed_persona),
	path('areas/<str:nombre>', views.detailed_persona),
	path('actividades/<int:id>', views.detailed_persona),
	path('notas/<int:id>', views.detailed_persona)
]
