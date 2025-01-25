import urllib.request
import json
from .models import Pokemon_Price
from django.contrib.auth import login
from .dao import Usuario, Venta #Se encarga de la interaccion con la DB

#-----------------------------------------------------------------------------------------------------------------------------------------------------
class PokemonDetails: #OBJETO POKEMON
    def __init__(self, data):
        self.number = data['id'] #Id/Numero de pokedex del pokemon
        self.name = data['name'].capitalize() #Nombre del pokemon
        self.element = ', '.join([type_data['type']['name'] for type_data in data['types']]) #Tipo de pokemon
        self.stats = data['stats'] #Guarda una lista con las estadisticas del pokemon
        #Se guardan las estadisticas en variables propias
        self.hp = self.stats[0]['base_stat'] #Vida del pokemon
        self.attack = self.stats[1]['base_stat'] #Valor de daño de ataque del pokemon
        self.defense = self.stats[2]['base_stat'] #Valor de defensa del pokemon
        self.speed = self.stats[5]['base_stat'] #Valor de velocidad del pokemon
        self.sprite = data['sprites']['front_default'] #Guarda el sprite 'front_default' del pokemon
        self.price = None #Representara el precio del pokemon

class Negocio:
    def realizar_venta(self, request):
        if request.user.is_authenticated:
            carrito = Carrito(request)
            total_venta = 0
            for key, value in carrito.carrito.items():
                total_venta += int(value["acumulado"])
            
            venta_dao = Venta()
            if venta_dao.guardar(request.user, total_venta):
                carrito.limpiar()
                return True
        
        return False
    
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
    
    def agregar(self, pokemonNumber):
        obtenerPokemon = ObtenerPokemons()
        pokemon = obtenerPokemon.pokemon_por_id(pokemonNumber)
        id = str(pokemon.number)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "pokemon_id": pokemon.number,
                "nombre": pokemon.name,
                "acumulado": pokemon.price,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += pokemon.price
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, pokemonNumber):
        id = str(pokemonNumber)
       
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, pokemonNumber):
        obtenerPokemon = ObtenerPokemons()
        pokemon = obtenerPokemon.pokemon_por_id(pokemonNumber)
        id = str(pokemon.number)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= pokemon.price
            if self.carrito[id]["cantidad"] <= 0: 
                self.eliminar(pokemon)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
#-----------------------------------------------------------------------------------------------------------------------------------------------------
class ObtenerPokemons: #CLASE QUE DEVUELVE OBJETOS POKEMONES
    def obtener_datos(self, pokemon_url): #Obtiene los datos de los pokemones solicitados de la API 
        url_pokemon = urllib.request.Request(pokemon_url) 
        url_pokemon.add_header('User-Agent', 'charmander')
        source = urllib.request.urlopen(url_pokemon).read()
        data = json.loads(source)
        pokemon = PokemonDetails(data)

        return self.completar_con_precio(pokemon)

    def completar_con_precio(self, pokemon): #Le asigna un valor al atributo price del pokemon
        try:
            price = Pokemon_Price.objects.get(pokedexNumber=pokemon.number).price
            pokemon.price = float(price)
        except Pokemon_Price.DoesNotExist:
            pokemon.price = None

        return pokemon #Devuelve el pokemon con el valor del atributo ya asignado

    def pokemon_por_cantidad(self, cantPokemons, offset=0): #Obtiene pokemones en base a la cantidad que se busque. Busqueda general
        url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/?limit={cantPokemons}&offset={offset}')
        url_pokeapi.add_header('User-Agent', 'charmander')
        source = urllib.request.urlopen(url_pokeapi).read()
        list_of_data = json.loads(source)

        pokemons = []
        for pokemon in list_of_data['results']:
            pokemon = self.obtener_datos(pokemon['url'])
            pokemons.append(pokemon)

        return pokemons #Devuelve diccionario con objetos pokemon
    
    def pokemon_por_id(self, id): #Obtiene pokemones en base a la cantidad que se busque. Busqueda general
        url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{id}')
        url_pokeapi.add_header('User-Agent', 'charmander')
        source = urllib.request.urlopen(url_pokeapi).read()
        data = json.loads(source)
        pokemon = PokemonDetails(data)

        return self.completar_con_precio(pokemon) #Devuelve diccionario con objetos pokemon

    def pokemon_por_nombre(self, nombre): #Obtiene un pokemon por su nombre
        url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{nombre}/')
        url_pokeapi.add_header('User-Agent', 'charmander')
        source = urllib.request.urlopen(url_pokeapi).read()
        data = json.loads(source)
        pokemon = PokemonDetails(data)

        return self.completar_con_precio(pokemon)  #Devuelve un objeto pokemon

class RegistrarUsuario: #CLASE PARA REGISTRAR USUARIOS
     def registrar(self, request, form): 
        #Se accede a los datos del form y se asignan los valores en las variables
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        usuario = Usuario() #Se instancia la clase Usuario del .dao
    
        user = usuario.crear(username, password)
        if user:
            login(request, user)
            return {'success': True, 'error_message': None}
        else:
            return {'success': False, 'error_message': 'No se pudo crear el usuario'}
        
class LoguearUsuario: #CLASE PARA LOGUEAR USUARIOS
    def loguear_usuario(self, request, form):
        #Se accede a los datos del form y se asignan los valores en las variables
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        usuario = Usuario()#Se instancia la clase Usuario del .dao
        
        user = usuario.loguear(request, username, password)
        if user:
            login(request, user)
            return {'success': True, 'error_message': None}
        else:
            return {'success': False, 'error_message': 'Usuario o contraseña incorrectos'}
        

