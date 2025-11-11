from django.test import TestCase, Client
from django.urls import reverse

from .models import (
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
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('grafica_html', data)

    def test_error_sin_comunidad_ni_provincia(self):
        url = reverse('generar_grafica_apilada')
        response = self.client.post(url, {
            'anio': '2025',
            'color_sexo': 'true',
            'solo_mortales': 'false'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('error', data)

    def test_error_sin_anio(self):
        url = reverse('generar_grafica_apilada')
        response = self.client.post(url, {
            'comunidades[]': ['Andalucía'],
            'color_sexo': 'true',
            'solo_mortales': 'false'
        })
        self.assertEqual(response.status_code, 200)
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
        response = self.client.post(url, {
            'nacionalidades[]': ['España'],
            'anio_inicio': '2024',
            'anio_fin': '2025'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('grafica_html', response.json())

    def test_error_sin_nacionalidad(self):
        url = reverse('generar_grafica_circular')
        response = self.client.post(url, {
            'nacionalidades[]': [],
            'anio_inicio': '2024',
            'anio_fin': '2025'
        })
        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('grafica_html', data)

    def test_error_sin_anio(self):
        url = reverse('generar_grafica_lineas')
        response = self.client.post(url, {
            'anio': '',
            'solo_mortales': 'false'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('error', data)