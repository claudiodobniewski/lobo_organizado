from django.test import TestCase
from django.urls import reverse
from django.test import Client

from socios.models import Familia



def test_familia_nueva():
        '''Test creacion nueva familia'''

        familia = Familia.objects.create(
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
        return familia

class ListadoFamiliasViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_no_familias(self):
        """
        Si no existen familias, un mensaje debe indicarlo en pantalla
        """

        response = self.client.get(reverse('socios:familia_listado'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se encontro ninguna familia.")

        familia = test_familia_nueva()

        familia.save()

        response = self.client.get(reverse('socios:familia_listado'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No se encontro ninguna familia.")
        self.assertContains(response, "Los Lopez")



