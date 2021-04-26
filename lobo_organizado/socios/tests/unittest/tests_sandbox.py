from django.test import TestCase,TransactionTestCase, client
import unittest
from django.test import Client
from .models import Familia, Socio, Observaciones
from django.contrib.auth.models import User

# Create your tests here.

class SocioTestCase(TransactionTestCase ):

    def setUp(self):
        self.familia = Familia.objects.create(
            familia_crm_id="Los Lopez",
            crm_id=33,
            direccion_calle="malabia 1500",
            direccion_numero="1234",
            direccion_depto="depto 4",
            direccion_localidad="San Miguel",
            direccion_provincia="Bs AS",
            contacto="saraza@gmail.com",
            eliminado=False
            )
        familia1 = Familia.objects.get(familia_crm_id="Los Lopez")

        self.socio = Socio.objects.create(
            nombres="lion", 
            apellidos="roar",
            dni="12345678",
            familia=self.familia,
            categoria=1,
            rama=0)

    def test_listado_familia(self):
        """Carga pantalla familia"""

        User.objects.create_superuser("claudio",email="claudiojd@gmail.com",password="sofijuli")
        c = Client()
        session = self.client.session
        
        response = c.login(username='claudio', password='sofijuli')
        print(response)
        

        
        # Issue a GET request.
        response = c.get('familia/1', follow=True)
        print(response.content)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context['socios']), 5)