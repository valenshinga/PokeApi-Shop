from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from .forms import buscar_Pokemon
from django.contrib.auth import logout
from .negocio import RegistrarUsuario, ObtenerPokemons, LoguearUsuario, Carrito, Negocio
from django.http import Http404, JsonResponse
from django.contrib import messages

class SignUpView(View): 
    template_name = 'signup.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        print(form.data) 
        
        if form.is_valid():
            result = RegistrarUsuario().registrar(request, form)
            if result['success']:
                return redirect('tienda')
            else:
                return self.render_error(request, form, result['error_message'])
        else:
            return self.render_error(request, form, "El formulario no es válido.")

    def render_error(self, request, form, error_message):
        return render(request, self.template_name, {
            'form': form,
            'error': error_message
        })

class SignInView(View):
    template_name = 'signin.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            loguear_usuario = LoguearUsuario()
            result = loguear_usuario.loguear_usuario(request, form)
            if result['success']:
                return redirect('tienda')
            else:
                return self.render_error(request, form, result['error_message'])
        else:
            return self.render_error(request, form, 'El formulario no es válido')

    def render_error(self, request, form, error_message):
        return render(request, self.template_name, {
            'form': form,
            'error': error_message
        })
        
class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect('tienda')

class TiendaView(View):
    template_name = 'tienda.html'

    def get(self, request):
        offset = int(request.GET.get('offset', 0))  # Obtén el valor del parámetro offset de la URL.
        pokemon_count = 20  # Cantidad de Pokémon a cargar en cada iteración.

        obtener_pokemons = ObtenerPokemons()
        pokemons = obtener_pokemons.pokemon_por_cantidad(pokemon_count, offset)  # Pasa el valor del offset

        return render(request, self.template_name, {
            "pokemons": pokemons,
            "offset": offset,
            "pokemon_count": pokemon_count,
        })
    
    def post(self, request):
        offset = int(request.GET.get('offset', 0))  # Obtén el offset de la URL
        obtener_pokemons = ObtenerPokemons()
        pokemons = obtener_pokemons.pokemon_por_cantidad(20, offset)  # Pasa el offset
        # Devuelve una respuesta JSON con los nuevos Pokémon
        return JsonResponse({"pokemons": [pokemon.__dict__ for pokemon in pokemons]})

class BuscarPokemonView(View):
    template_name = 'buscar_pokemon.html'

    def get(self, request):
        form = buscar_Pokemon()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = buscar_Pokemon(request.POST)
        
        if form.is_valid():
            pokemon = ObtenerPokemons().pokemon_por_nombre(form.cleaned_data['name'])
            return render(request, self.template_name, {'data': pokemon, 'form': form})
        return render(request, self.template_name, {'form': form})
    
class AgregarPokemonView(View):
    def get(self, request, pokemonNumber):
        carrito = Carrito(request)
        try:
            carrito.agregar(pokemonNumber)
        except Http404:
            messages.error(request, 'El Pokémon que intentas agregar no existe.')
        return redirect('tienda')

class EliminarPokemonView(View):
    def get(self, request, pokemonNumber):
        carrito = Carrito(request)
        try:
            producto = pokemonNumber
            carrito.eliminar(producto)
        except Http404:
            messages.error(request, 'El Pokémon que intentas eliminar no existe.')
        return redirect('tienda')

class RestarPokemonView(View):
    def get(self, request, pokemonNumber):
        carrito = Carrito(request)
        try:
            producto = pokemonNumber
            carrito.restar(producto)
        except Http404:
            messages.error(request, 'El Pokémon que intentas restar no existe.')
        return redirect('tienda')

class LimpiarCarritoView(View):
    def get(self, request):
        carrito = Carrito(request)
        carrito.limpiar()
        return redirect('tienda')
    
class GuardarVentaView(View):
    def get(self, request):
        negocio = Negocio()
        if negocio.realizar_venta(request):
            return redirect('venta_exitosa')
        else:
            return redirect('venta_fallida')
        
class VentaExitosaView(View):
    template_name = 'venta_exitosa.html'

    def get(self, request):
        return render(request, self.template_name)
    
class VentaFallidaView(View):
    template_name = 'venta_fallida.html'

    def get(self, request):
        return render(request, self.template_name)
    
