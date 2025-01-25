from django.db import models
from django.contrib.auth.models import User

class registro_Venta(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)  
    importe = models.DecimalField(max_digits=10, decimal_places=2)  
    fecha_venta = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Usuario: {self.username} - ${self.importe} - {self.fecha_venta}"

class Pokemon_Price(models.Model):
    pokedexNumber = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del Pokémon
   
    def __str__(self):
        return f"{self.pokedexNumber} - ${self.price}"
    
