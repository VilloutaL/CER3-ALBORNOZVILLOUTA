from django.db import models

# Create your models here.
class Evento(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    TIPO_CHOICES={
        ("V","Vacaciones"),
        ("F","Feriado"),
        ("SA","Suspension de Actividades"),
        ("SAPM","Suspension de actividades PM"),
        ("SE","Suspension de Evaluaciones"),
        ("C","Ceremonia"),
        ("EDDA","EDDA"),
        ("EV","Evaluacion"),
        ("AY","Ayudantias"),
        ("HA","Hito Academico"),
        ("SAC","Secretaria Academica"),
        ("OAI","OAI"),
    }
    tipo = models.CharField(max_length=20,choices=TIPO_CHOICES)
    SEGMENTO_CHOICES={
        ("CU","Comunidad USM"),
        ("ES","Estudiante"),
        ("PR","Profesor"),
        ("JC","Jefe de Carrera"),
    }
    segmento = models.CharField(max_length=20, choices=SEGMENTO_CHOICES)