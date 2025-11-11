from django.urls import path
from home.api.views import (
    home_endpoint,
    GenerarGraficaApiladaAPIView,
    GenerarGraficaCircularAPIView,
    GenerarGraficaLineasAPIView,
    GenerarDiagramaDispersionAPIView,
    GenerarMapaAPIView,
    GenerarHistogramaAPIView,
    GenerarRadarAPIView,
    ComparativaSklearnAPIView,
    GenerarMapaHotspotsAPIView,
    GenerarKMeansAPIView,
    GenerarTreeAPIView
)

urlpatterns = [
    path('', home_endpoint),
    path('generar_grafica_apilada/', GenerarGraficaApiladaAPIView.as_view(), name='generar_grafica_apilada'),
    path('generar_grafica_circular/', GenerarGraficaCircularAPIView.as_view(), name='generar_grafica_circular'),
    path('generar_grafica_lineas/', GenerarGraficaLineasAPIView.as_view(), name='generar_grafica_lineas'),
    path('generar_diagrama_dispersion/', GenerarDiagramaDispersionAPIView.as_view(), name='generar_diagrama_dispersion'),
    path('generar_mapa/', GenerarMapaAPIView.as_view(), name='generar_mapa'),
    path('generar_histograma/', GenerarHistogramaAPIView.as_view(), name='generar_histograma'),
    path('generar_radar/', GenerarRadarAPIView.as_view(), name='generar_radar'),
    path('comparativa_sklearn/', ComparativaSklearnAPIView.as_view(), name='comparativa_sklearn'),
    path('generar_mapa_hotspots/', GenerarMapaHotspotsAPIView.as_view(), name='generar_mapa_hotspots'),
    path('generar_kmeans/', GenerarKMeansAPIView.as_view(), name='generar_kmeans'),
    path('generar_tree/', GenerarTreeAPIView.as_view(), name='generar_tree'),
]
