from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from home.services.graficas import (
    home,
    generar_grafica_apilada,
    generar_grafica_circular,
    generar_grafica_lineas,
    generar_diagrama_dispersion,
    generar_mapa,
    generar_histograma,
    generar_radar,
    comparativa_sklearn,
    generar_mapa_hotspots,
    generar_kmeans,
    generar_tree
)

def home_endpoint(request):
    return home(request)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarGraficaApiladaAPIView(APIView):
    def post(self, request):
        comunidades = request.data.get('comunidades', [])
        provincias = request.data.get('provincias', [])
        anio = request.data.get('anio')
        colorsexo = request.data.get('colorsexo')
        solomortales = request.data.get('solomortales', True)
        resultado = generar_grafica_apilada(comunidades, provincias, anio, colorsexo, solomortales)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarGraficaCircularAPIView(APIView):
    def post(self, request):
        nacionalidades = request.data.get('nacionalidades', [])
        anioinicio = request.data.get('anioinicio')
        aniofin = request.data.get('aniofin')
        resultado = generar_grafica_circular(nacionalidades, anioinicio, aniofin)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarGraficaLineasAPIView(APIView):
    def post(self, request):
        anio = request.data.get('anio')
        solomortales = request.data.get('solomortales', True)
        resultado = generar_grafica_lineas(anio, solomortales)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarDiagramaDispersionAPIView(APIView):
    def post(self, request):
        colorsexo = request.data.get('colorsexo')
        solomortales = request.data.get('solomortales', True)
        mostrarlinea = request.data.get('mostrarlinea', False)
        resultado = generar_diagrama_dispersion(colorsexo, solomortales, mostrarlinea)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarMapaAPIView(APIView):
    def post(self, request):
        solomortales = request.data.get('solomortales', True)
        lugares = request.data.get('lugares', [])
        resultado = generar_mapa(solomortales, lugares)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarHistogramaAPIView(APIView):
    def post(self, request):
        solomortales = request.data.get('solomortales', True)
        dias = request.data.get('dias', [])
        resultado = generar_histograma(solomortales, dias)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarRadarAPIView(APIView):
    def post(self, request):
        filtro = request.data.get('filtro')
        resultado = generar_radar(filtro)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class ComparativaSklearnAPIView(APIView):
    def post(self, request):
        actividad = request.data.get('actividad')
        localizacion = request.data.get('localizacion')
        zonavigilada = request.data.get('zonavigilada')
        factorriesgo = request.data.get('factorriesgo')
        intervencion = request.data.get('intervencion')
        edad = request.data.get('edad')
        resultado = comparativa_sklearn(
            actividad=actividad,
            localizacion=localizacion,
            zonavigilada=zonavigilada,
            factorriesgo=factorriesgo,
            intervencion=intervencion,
            edad=edad
        )
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarMapaHotspotsAPIView(APIView):
    def post(self, request):
        anio_inicio = request.data.get('anio-inicio-hotspots')
        anio_fin = request.data.get('anio-fin-hotspots')
        resultado = generar_mapa_hotspots(anio_inicio, anio_fin)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarKMeansAPIView(APIView):
    def post(self, request):
        anio_inicio = request.data.get('anio-inicio')
        anio_fin = request.data.get('anio-fin')
        resultado = generar_kmeans(anio_inicio, anio_fin)
        return Response(resultado)

@method_decorator(csrf_exempt, name='dispatch')
class GenerarTreeAPIView(APIView):
    def post(self, request):
        filtros= request.data.get('filtro')
        resultado = generar_tree(filtros)
        return Response(resultado)
