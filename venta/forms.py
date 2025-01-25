from django import forms

class buscar_Pokemon(forms.Form):
    name = forms.CharField(label="Nombre del pokemon", max_length=100)

