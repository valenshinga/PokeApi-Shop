from django.urls import path
from .views import  TiendaView, BuscarPokemonView, SignUpView, SignInView, SignOutView, AgregarPokemonView, RestarPokemonView,  EliminarPokemonView, LimpiarCarritoView, GuardarVentaView, VentaExitosaView, VentaFallidaView

urlpatterns = [
    path('', TiendaView.as_view(), name="tienda"),
    path('buscar_pokemon/', BuscarPokemonView.as_view(), name="buscar_pokemones"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('logout/', SignOutView.as_view(), name='logout'), 
    path('agregar/<int:pokemonNumber>/', AgregarPokemonView.as_view(), name="add"),
    path('eliminar/<int:pokemonNumber>/', EliminarPokemonView.as_view(), name="del"),
    path('restar/<int:pokemonNumber>/', RestarPokemonView.as_view(), name="sub"),
    path('limpiar/', LimpiarCarritoView.as_view(), name="cls"),
    path('guardar/', GuardarVentaView.as_view(), name="guardar"),
    path('ventaExitosa/', VentaExitosaView.as_view(), name="venta_exitosa"),
    path('ventaFallida/', VentaFallidaView.as_view(), name="venta_fallida"),
]