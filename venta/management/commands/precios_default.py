from django.core.management.base import BaseCommand
from venta.models import Pokemon_Price

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # Set the initial value for pokedexNumber
        current_pokedex_number = 10001
        current_price = 518.50
        end_pokedex_number = 10275

    # Create and save records
        while current_pokedex_number <= end_pokedex_number:
        # Create a new instance of the model
            new_record = Pokemon_Price(pokedexNumber=current_pokedex_number, price=current_price)
        
        # Save the record to the database
            new_record.save()

        # Increment values for the next record
            current_pokedex_number += 1
            current_price += 0.50