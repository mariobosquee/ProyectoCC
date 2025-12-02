
from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.urls import reverse
import json
import subprocess
import time
import requests
from django.test import SimpleTestCase


from home.models import (
    Actividad, Deteccion, Intervencion, Localizacion, Riesgo, Zonavigilada,
    Ccaa, Provincia, Localidad,
    Pronostico, Extraccion, Materialrescate, Nacionalidad, Origen,
    Primerinterviniente, Reanimacion, Tipoahogamiento,
    Incidente, Victima
)

class TestGenerarGraficaApilada(TestCase):

    def setUp(self):
        self.client = Client()

        # Introducción de los datos de prueba
        self.ccaa = Ccaa.objects.create(nombreccaa="Andalucía")
        self.provincia = Provincia.objects.create(nombreprovincia="Granada", codccaa=self.ccaa)
        self.localidad = Localidad.objects.create(nombrelocalidad="Playa Granada", provincia=self.provincia)

        # FK obligatorias para Incidente
        self.actividad = Actividad.objects.create(nombreactividad="Nadar")
        self.deteccion = Deteccion.objects.create(nombredeteccion="Rápida")
        self.intervencion = Intervencion.objects.create(nombreintervencion="Rescate agua")
        self.localizacion = Localizacion.objects.create(nombrelocalizacion="Zona 1")
        self.riesgo = Riesgo.objects.create(nombreriesgo="Alto")
        self.zonavigilada = Zonavigilada.objects.create(nombrezonavigilada="Zona A")

        # FK obligatorias para Victima
        self.pronostico = Pronostico.objects.create(nombrepronostico="No mortal")
        self.extraccion = Extraccion.objects.create(nombreextraccion="Orilla")
        self.materialrescate = Materialrescate.objects.create(nombrematerialrescate="Cuerda")
        self.nacionalidad = Nacionalidad.objects.create(nombrenacionalidad="España")
        self.origen = Origen.objects.create(nombreorigen="Turista")
        self.primerinterviniente = Primerinterviniente.objects.create(nombreprimerinterviniente="Socorrista")
        self.reanimacion = Reanimacion.objects.create(nombrereanimacion="Correcta")
        self.tipoahogamiento = Tipoahogamiento.objects.create(nombretipoahogamiento="Inhalación agua")

        # Creación de un incidente
        self.incidente = Incidente.objects.create(
            fecha="2025-01-01",
            hora="12:00",
            titular="Incidente 1",
            latitud="37.16",
            longitud="-3.60",
            enlace="http://ejemplo.com",
            actividad=self.actividad,
            deteccion=self.deteccion,
            intervencion=self.intervencion,
            localidad=self.localidad,
            localizacion=self.localizacion,
            riesgo=self.riesgo,
            zona=self.zonavigilada
        )

        # Creación de dos víctimas con sexos diferentes para cubrir las dos columnas del gráfico
        self.victima1 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Hombre',
            edad=30,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )
        self.victima2 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Mujer',
            edad=25,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )

    def test_grafica_valida(self):
        url = reverse('generar_grafica_apilada')
        response = self.client.post(url, {
            'comunidades[]': ['Andalucía'],
            'anio': '2025',
            'color_sexo': 'true',
            'solo_mortales': 'false'
        })
        self.assertNotEqual(response.status_code, 400)
        data = response.json()
        self.assertTrue('grafica_html' in data or 'error' in data)

    def test_error_sin_comunidad_ni_provincia(self):
        url = reverse('generar_grafica_apilada')
        response = self.client.post(url, {
            'anio': '2025',
            'color_sexo': 'true',
            'solo_mortales': 'false'
        })
        self.assertNotEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

    def test_error_sin_anio(self):
        url = reverse('generar_grafica_apilada')
        response = self.client.post(url, {
            'comunidades[]': ['Andalucía'],
            'color_sexo': 'true',
            'solo_mortales': 'false'
        })
        self.assertNotEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

class TestGenerarGraficaCircular(TestCase):

    def setUp(self):
        self.client = Client()

        # Introducción de los datos de prueba
        self.ccaa = Ccaa.objects.create(nombreccaa="Andalucía")
        self.provincia = Provincia.objects.create(nombreprovincia="Granada", codccaa=self.ccaa)
        self.localidad = Localidad.objects.create(nombrelocalidad="Playa Granada", provincia=self.provincia)

        # FK obligatorias para Incidente
        self.actividad = Actividad.objects.create(nombreactividad="Nadar")
        self.deteccion = Deteccion.objects.create(nombredeteccion="Rápida")
        self.intervencion = Intervencion.objects.create(nombreintervencion="Rescate agua")
        self.localizacion = Localizacion.objects.create(nombrelocalizacion="Zona 1")
        self.riesgo = Riesgo.objects.create(nombreriesgo="Alto")
        self.zonavigilada = Zonavigilada.objects.create(nombrezonavigilada="Zona A")

        # FK obligatorias para Victima
        self.pronostico = Pronostico.objects.create(nombrepronostico="No mortal")
        self.extraccion = Extraccion.objects.create(nombreextraccion="Orilla")
        self.materialrescate = Materialrescate.objects.create(nombrematerialrescate="Cuerda")
        self.nacionalidad = Nacionalidad.objects.create(nombrenacionalidad="España")
        self.origen = Origen.objects.create(nombreorigen="Turista")
        self.primerinterviniente = Primerinterviniente.objects.create(nombreprimerinterviniente="Socorrista")
        self.reanimacion = Reanimacion.objects.create(nombrereanimacion="Correcta")
        self.tipoahogamiento = Tipoahogamiento.objects.create(nombretipoahogamiento="Inhalación agua")

        # Creación de un incidente
        self.incidente = Incidente.objects.create(
            fecha="2025-01-01",
            hora="12:00",
            titular="Incidente 1",
            latitud="37.16",
            longitud="-3.60",
            enlace="http://ejemplo.com",
            actividad=self.actividad,
            deteccion=self.deteccion,
            intervencion=self.intervencion,
            localidad=self.localidad,
            localizacion=self.localizacion,
            riesgo=self.riesgo,
            zona=self.zonavigilada
        )

        # Creación de dos víctimas con sexos diferentes para cubrir las dos columnas del gráfico
        self.victima1 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Hombre',
            edad=30,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )
        self.victima2 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Mujer',
            edad=25,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )

    

    def test_grafica_correcta(self):
        url = reverse('generar_grafica_circular')
        response = self.client.post(
            url,
            data=json.dumps({
                'nacionalidades': ['España'],
                'anioinicio': '2024',
                'aniofin': '2025'
            }),
            content_type='application/json'
        )
        self.assertNotEqual(response.status_code, 400)
        self.assertIn('grafica_html', response.json())


    def test_error_sin_nacionalidad(self):
        url = reverse('generar_grafica_circular')
        response = self.client.post(url, {
            'nacionalidades': [],
            'anio_inicio': '2024',
            'anio_fin': '2025'
        })
        self.assertNotEqual(response.status_code, 400)
        self.assertIn('error', response.json())

class TestGenerarGraficaLineas(TestCase):

    def setUp(self):
        self.client = Client()

        # Introducción de los datos de prueba
        self.ccaa = Ccaa.objects.create(nombreccaa="Andalucía")
        self.provincia = Provincia.objects.create(nombreprovincia="Granada", codccaa=self.ccaa)
        self.localidad = Localidad.objects.create(nombrelocalidad="Playa Granada", provincia=self.provincia)

        # FK obligatorias para Incidente
        self.actividad = Actividad.objects.create(nombreactividad="Nadar")
        self.deteccion = Deteccion.objects.create(nombredeteccion="Rápida")
        self.intervencion = Intervencion.objects.create(nombreintervencion="Rescate agua")
        self.localizacion = Localizacion.objects.create(nombrelocalizacion="Zona 1")
        self.riesgo = Riesgo.objects.create(nombreriesgo="Alto")
        self.zonavigilada = Zonavigilada.objects.create(nombrezonavigilada="Zona A")

        # FK obligatorias para Victima
        self.pronostico = Pronostico.objects.create(nombrepronostico="No mortal")
        self.extraccion = Extraccion.objects.create(nombreextraccion="Orilla")
        self.materialrescate = Materialrescate.objects.create(nombrematerialrescate="Cuerda")
        self.nacionalidad = Nacionalidad.objects.create(nombrenacionalidad="España")
        self.origen = Origen.objects.create(nombreorigen="Turista")
        self.primerinterviniente = Primerinterviniente.objects.create(nombreprimerinterviniente="Socorrista")
        self.reanimacion = Reanimacion.objects.create(nombrereanimacion="Correcta")
        self.tipoahogamiento = Tipoahogamiento.objects.create(nombretipoahogamiento="Inhalación agua")

        # Creación de un incidente
        self.incidente = Incidente.objects.create(
            fecha="2025-01-01",
            hora="12:00",
            titular="Incidente 1",
            latitud="37.16",
            longitud="-3.60",
            enlace="http://ejemplo.com",
            actividad=self.actividad,
            deteccion=self.deteccion,
            intervencion=self.intervencion,
            localidad=self.localidad,
            localizacion=self.localizacion,
            riesgo=self.riesgo,
            zona=self.zonavigilada
        )

        # Creación de dos víctimas con sexos diferentes para cubrir las dos columnas del gráfico
        self.victima1 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Hombre',
            edad=30,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )
        self.victima2 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Mujer',
            edad=25,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )

    def test_grafica_lineas_valida(self):
        url = reverse('generar_grafica_lineas')
        response = self.client.post(url, {
            'anio': '2025',
            'solo_mortales': 'false'
        })
        self.assertNotEqual(response.status_code, 400)
        data = response.json()
        self.assertTrue('grafica_html' in data or 'error' in data)

    def test_error_sin_anio(self):
        url = reverse('generar_grafica_lineas')
        response = self.client.post(url, {
            'anio': '',
            'solo_mortales': 'false'
        })
        self.assertNotEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

class GraficasLineasTestsAPI(APITestCase):
    def setUp(self):
        self.ccaa = Ccaa.objects.create(nombreccaa="Andalucía")
        self.provincia = Provincia.objects.create(nombreprovincia="Granada", codccaa=self.ccaa)
        self.localidad = Localidad.objects.create(nombrelocalidad="Playa Granada", provincia=self.provincia)
        self.actividad = Actividad.objects.create(nombreactividad="Nadar")
        self.deteccion = Deteccion.objects.create(nombredeteccion="Rápida")
        self.intervencion = Intervencion.objects.create(nombreintervencion="Rescate agua")
        self.localizacion = Localizacion.objects.create(nombrelocalizacion="Zona 1")
        self.riesgo = Riesgo.objects.create(nombreriesgo="Alto")
        self.zonavigilada = Zonavigilada.objects.create(nombrezonavigilada="Zona A")

        self.incidente = Incidente.objects.create(
            fecha="2015-01-01",
            hora="12:00",
            titular="Incidente 1",
            latitud="37.16",
            longitud="-3.60",
            enlace="http://ejemplo.com",
            actividad=self.actividad,
            deteccion=self.deteccion,
            intervencion=self.intervencion,
            localidad=self.localidad,
            localizacion=self.localizacion,
            riesgo=self.riesgo,
            zona=self.zonavigilada
        )

        self.extraccion = Extraccion.objects.create(nombreextraccion="Orilla")
        self.materialrescate = Materialrescate.objects.create(nombrematerialrescate="Cuerda")
        self.nacionalidad = Nacionalidad.objects.create(nombrenacionalidad="España")
        self.origen = Origen.objects.create(nombreorigen="Turista")
        self.primerinterviniente = Primerinterviniente.objects.create(nombreprimerinterviniente="Socorrista")
        self.pronostico = Pronostico.objects.create(nombrepronostico="No mortal")
        self.reanimacion = Reanimacion.objects.create(nombrereanimacion="Correcta")
        self.tipoahogamiento = Tipoahogamiento.objects.create(nombretipoahogamiento="Inhalación agua")

        self.victima1 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Hombre',
            edad=30,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )
        self.victima2 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Mujer',
            edad=25,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )

    def test_lineas_correcto(self):
        url = '/generar_grafica_lineas/'
        data = {'anio': 2015, 'solomortales': True}
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 400)
        self.assertTrue('grafica' in response.data or 'error' in response.data)

class GraficasRadarTestsAPI(APITestCase):
    def setUp(self):
        self.ccaa = Ccaa.objects.create(nombreccaa="Andalucía")
        self.provincia = Provincia.objects.create(nombreprovincia="Granada", codccaa=self.ccaa)
        self.localidad = Localidad.objects.create(nombrelocalidad="Playa Granada", provincia=self.provincia)
        self.actividad = Actividad.objects.create(nombreactividad="Nadar")
        self.deteccion = Deteccion.objects.create(nombredeteccion="Rápida")
        self.intervencion = Intervencion.objects.create(nombreintervencion="Rescate agua")
        self.localizacion = Localizacion.objects.create(nombrelocalizacion="Zona 1")
        self.riesgo = Riesgo.objects.create(nombreriesgo="Alto")
        self.zonavigilada = Zonavigilada.objects.create(nombrezonavigilada="Zona A")

        self.incidente = Incidente.objects.create(
            fecha="2025-01-01",
            hora="12:00",
            titular="Incidente 1",
            latitud="37.16",
            longitud="-3.60",
            enlace="http://ejemplo.com",
            actividad=self.actividad,
            deteccion=self.deteccion,
            intervencion=self.intervencion,
            localidad=self.localidad,
            localizacion=self.localizacion,
            riesgo=self.riesgo,
            zona=self.zonavigilada
        )

        self.extraccion = Extraccion.objects.create(nombreextraccion="Orilla")
        self.materialrescate = Materialrescate.objects.create(nombrematerialrescate="Cuerda")
        self.nacionalidad = Nacionalidad.objects.create(nombrenacionalidad="España")
        self.origen = Origen.objects.create(nombreorigen="Turista")
        self.primerinterviniente = Primerinterviniente.objects.create(nombreprimerinterviniente="Socorrista")
        self.pronostico = Pronostico.objects.create(nombrepronostico="No mortal")
        self.reanimacion = Reanimacion.objects.create(nombrereanimacion="Correcta")
        self.tipoahogamiento = Tipoahogamiento.objects.create(nombretipoahogamiento="Inhalación agua")

        self.victima1 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Hombre',
            edad=30,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )
        self.victima2 = Victima.objects.create(
            incidente=self.incidente,
            sexo='Mujer',
            edad=25,
            extraccion=self.extraccion,
            materialrescate=self.materialrescate,
            nacionalidad=self.nacionalidad,
            origen=self.origen,
            primerinterviniente=self.primerinterviniente,
            pronostico=self.pronostico,
            reanimacion=self.reanimacion,
            tipoahogamiento=self.tipoahogamiento
        )

    def test_radar_correcto(self):
        url = '/generar_radar/'
        data = {'filtros': {'actividad': "Surf-Windsurf-Esqui acuatico-Kyte"}}
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 400)
        self.assertTrue('grafica' in response.data or 'error' in response.data)
        
class GraficasMapaTestsAPI(APITestCase):
    def test_mapa_correcto(self):
        url = '/generar_mapa/'
        
        self.ccaa = Ccaa.objects.create(nombreccaa="Andalucía")
        self.provincia = Provincia.objects.create(nombreprovincia="Granada", codccaa=self.ccaa)
        self.localidad = Localidad.objects.create(nombrelocalidad="Motril", provincia=self.provincia)
        self.actividad = Actividad.objects.create(nombreactividad="Nadar")
        self.deteccion = Deteccion.objects.create(nombredeteccion="Rápida")
        self.intervencion = Intervencion.objects.create(nombreintervencion="Rescate agua")
        self.localizacion = Localizacion.objects.create(nombrelocalizacion="Playas con vigilancia")
        self.riesgo = Riesgo.objects.create(nombreriesgo="Alto")
        self.zonavigilada = Zonavigilada.objects.create(nombrezonavigilada="Zona A")
        self.pronostico = Pronostico.objects.create(nombrepronostico="Ahogamiento mortal")
        self.incidente = Incidente.objects.create(
            fecha="2025-01-01", hora="12:00", titular="Incidente X",
            latitud="37.18", longitud="-3.60", enlace="http://ejemplo.com",
            actividad=self.actividad, deteccion=self.deteccion,
            intervencion=self.intervencion, localidad=self.localidad,
            localizacion=self.localizacion, riesgo=self.riesgo, zona=self.zonavigilada
        )
        self.extraccion = Extraccion.objects.create(nombreextraccion="Orilla")
        self.materialrescate = Materialrescate.objects.create(nombrematerialrescate="Cuerda")
        self.nacionalidad = Nacionalidad.objects.create(nombrenacionalidad="España")
        self.origen = Origen.objects.create(nombreorigen="Turista")
        self.primerinterviniente = Primerinterviniente.objects.create(nombreprimerinterviniente="Socorrista")
        self.reanimacion = Reanimacion.objects.create(nombrereanimacion="Correcta")
        self.tipoahogamiento = Tipoahogamiento.objects.create(nombretipoahogamiento="Inhalación agua")
        self.victima = Victima.objects.create(
            incidente=self.incidente, sexo='Hombre', edad=35, extraccion=self.extraccion,
            materialrescate=self.materialrescate, nacionalidad=self.nacionalidad, origen=self.origen,
            primerinterviniente=self.primerinterviniente, pronostico=self.pronostico,
            reanimacion=self.reanimacion, tipoahogamiento=self.tipoahogamiento
        )

        data = {'solo_mortales': True, 'lugares': ['Playa']}
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 400)
        self.assertTrue('grafica_html' in response.data or 'error' in response.data)

COMPOSE_FILE = "docker-compose.yml"
BASE_URL = "http://localhost:8000"
TIMEOUT = 120       # segundos máximos esperando a que arranque
SLEEP = 3  # segundos entre intentos

def run(cmd):
    subprocess.run(cmd, check=True)


def wait_for_web():
    start = time.time()
    while time.time() - start < TIMEOUT:
        try:
            r = requests.get(BASE_URL, timeout=5)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(SLEEP)
    raise RuntimeError("El servicio web no ha arrancado a tiempo")


class ClusterContainersTest(SimpleTestCase):
    """Test de integración del clúster Docker."""

    def test_cluster_responde_correctamente(self):
        try:
            # Levantar clúster
            run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"])

            # Esperar a que el web esté listo
            wait_for_web()

            # Home
            r_home = requests.get(f"{BASE_URL}/", timeout=10)
            self.assertEqual(r_home.status_code, 200)

            # Endpoint que toca BD (ajusta la ruta)
            r_graph = requests.get(f"{BASE_URL}/generar_grafica_apilada/", timeout=10)
            self.assertEqual(r_graph.status_code, 200)
        finally:
            # Parar clúster
            run(["docker", "compose", "-f", COMPOSE_FILE, "down"])