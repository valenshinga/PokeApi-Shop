#PATRON DE DISEÑO REPOSITORY

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import registro_Venta

class Usuario: #CLASE ENCARGADA DE INTERACTUAR CON EL MODELO User DE LA DB
    def crear(self, username, password): #Metodo para crear un nuevo usuario
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return user
        except IntegrityError:
            return None
    
    def loguear(self, request, username, password): #Metodo para loguear un usuario
        user = authenticate(request, username=username, password=password)
        return user

class Venta:
    def guardar(self, user, importe):
        try:
            venta = registro_Venta(username=user, importe=importe)
            venta.save()
            return True
        except Exception as e:
            print(f"Error al guardar el registro de venta: {str(e)}")
            return False
