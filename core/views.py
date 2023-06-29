from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Profesor,Estudiante
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from core.forms import EstudianteForm, NotaForm, AnotacionForm, ProfesorForm
#@login_required

def asistencia(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        asistencia_data = request.POST.getlist('asistencia')

        # Actualizar la asistencia en la base de datos
        for data in asistencia_data:
            id_Estudiante, asistencia = data.split('-')
            estudiante = Estudiante.objects.get(pk=id_Estudiante)
            estudiante.asistencia = asistencia == 'presente'
            estudiante.save()


    # Obtener todos los estudiantes de la base de datos
    estudiantes = Estudiante.objects.all()

    # Renderizar la plantilla con los datos de los estudiantes
    datos = {
        'estudiantes': estudiantes
    }
    return render(request, 'asistencia.html', datos)



def is_staff(user):
    return (user.is_authenticated and user.is_superuser)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            # Mostrar un mensaje de error de inicio de sesión
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    
def menu(request):
    return render(request,'menu.html')

def cursos(request):
    return render(request,'cursos.html')

def notas(request):
    datos = {
        'form1': NotaForm()
    }

    if request.method == 'POST':
        formulario1 =  NotaForm(request.POST or None, request.FILES or None)

        if formulario1.is_valid():
            formulario1.save() #insert a la BD
            datos['mensaje'] = 'Se guardó la nota'
        else:
            datos['mensaje'] = 'NO se guardó la nota'

    return render(request,'notas.html' ,datos)

def anotaciones(request):
    datos = {
        'form2': AnotacionForm()
    }

    if request.method == 'POST':
        formulario2 =  NotaForm(request.POST or None, request.FILES or None)

        if formulario2.is_valid():
            formulario2.save() #insert a la BD
            datos['mensaje'] = 'Se guardó la anotacion'
        else:
            datos['mensaje'] = 'NO se guardó la anotacion'
    
    return render(request,'anotaciones.html', datos)

def donacion(request):
    return render(request,'Donacion.html')

def adminalumno(request):
    datos = {
        'form': EstudianteForm()
    }

    if request.method == 'POST':
        formulario =  EstudianteForm(request.POST or None, request.FILES or None)

        if formulario.is_valid():
            formulario.save() #insert a la BD
            datos['mensaje'] = 'Se guardó el alumno'
        else:
            datos['mensaje'] = 'NO se guardó el alumno'

    return render(request,'admin/adminalumno.html',datos)

def adminasistencia(request):
    return render(request,'admin/adminasistencia.html')

def admincreacion(request):
    return render(request,'admin/admincreacion.html')

def adminprofesor(request):
    datos = {
        'form': ProfesorForm()
    }

    if request.method == 'POST':
        formulario =  ProfesorForm(request.POST or None, request.FILES or None)

        if formulario.is_valid():
            formulario.save() #insert a la BD
            datos['mensaje'] = 'Se guardó el profesor'
        else:
            datos['mensaje'] = 'NO se guardó el profesor'
    
    return render(request,'admin/adminprofesor.html' ,datos)