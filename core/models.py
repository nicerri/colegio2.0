from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Admin(AbstractUser):
    admin_id = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15)
    cargo = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='administrador'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='administrador'
    )

    def __str__(self):
        return self.username

class Apoderado(models.Model):
    id_apoderado = models.AutoField(primary_key=True, default=0)
    nombre_apoderado = models.CharField(max_length=100,default=True)
    direccion = models.CharField(max_length=200, default='Dirección por defecto')
    telefono = models.CharField(max_length=15, default='000000000')
    correo = models.EmailField(default='example@example.com')

    def __str__(self):
        return str(self.id_apoderado)



class Estudiante(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    id_Estudiante = models.AutoField( primary_key=True, verbose_name='Id Estudiante')
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    asistencia = models.BooleanField(default=False)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)

    def __str__(self):
        return f'{self.primer_nombre} {self.primer_apellido}'




class Asistencia(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias',default=None)
    fecha = models.DateField(null=True)
    presente = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True, default=None)


    def __str__(self):
        estado = "Presente" if self.presente else "Ausente"
        return f"Asistencia de {self.estudiante.nombre} - {self.fecha} ({estado})"


class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='notas',default=None)
    asignatura = models.CharField(max_length=100, default='')
    valor = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    fecha = models.DateField(default=timezone.now)
    tipo_evaluacion = models.CharField(max_length=100,null=True)
    profesor = models.CharField(max_length=100, null=True)
    id_nota = models.AutoField(primary_key=True, default=None)


    def __str__(self):
        return f"Nota de {self.estudiante.nombre} - {self.asignatura}"


class Anotacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='anotaciones')
    fecha = models.DateField(null=True)
    mensaje = models.TextField()
    remitente = models.CharField(max_length=100)
    asunto = models.CharField(max_length=200)

    def __str__(self):
        return f"Anotación de {self.estudiante.nombre} - {self.asunto}"


class Profesor(models.Model):
    nombre = models.CharField(max_length=100,null=True)
    especialidad = models.CharField(max_length=100,null=True)
    correo = models.EmailField(default='example@example.com')
    id_profesor = models.AutoField(primary_key=True, default=None)

    def __str__(self):
        return self.nombre


class Colegio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    director = models.CharField(max_length=100)
    estudiantes = models.ManyToManyField(Estudiante, related_name='colegios')

    def __str__(self):
        return self.nombre
