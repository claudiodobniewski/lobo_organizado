from django.test import TestCase
from django.utils import timezone

from .models import Familia, Socio

class FamiliaTest(TestCase):



    def test_familia_nueva(self):
        '''Test creacion nueva familia'''

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

        #familia = Familia.objects.get(familia_crm_id="Los Lopez")

        print(self.familia)

        self.assertEqual(self.familia.familia_crm_id,"Los Lopez")