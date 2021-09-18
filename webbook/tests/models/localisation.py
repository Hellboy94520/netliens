from django.test import TestCase

from webbook.models import get_all_model_in_order, get_all_modelWithData_in_order, get_all_modelDataWithPosition_in_order
from webbook.models import Localisation, LocalisationData
from webbook.models import LanguageAvailable

class LocalisationModel(TestCase):
    def createLocalisationWithData(self, **kwargs):
        localisation = Localisation.objects.create(
            is_enable=True,
            parent=kwargs['parent'],
            order=kwargs['order']
        )
        localisationDataFr = LocalisationData.objects.create(
            name=kwargs['name'],
            resume=kwargs['resume'],
            localisation=localisation,
            language=LanguageAvailable.FR.value
        )
        localisationDataEn = LocalisationData.objects.create(
            name=kwargs['name'],
            resume=kwargs['resume'],
            localisation=localisation,
            language=LanguageAvailable.EN.value
        )
        return localisation, localisationDataFr, localisationDataEn

    def initLocalisationWithDataForTest(self):
        # Creation random localisation
        self.localisation_2, self.localisation_2_fr, self.localisation_2_en = self.createLocalisationWithData(
            parent=None,
            order=2,
            name="Localisation 2",
            resume="Localisation 2"
        )
        self.localisation_22, self.localisation_22_fr, self.localisation_22_en = self.createLocalisationWithData(
            parent=self.localisation_2,
            order=2,
            name="Localisation 22",
            resume="Localisation 22"
        )
        self.localisation_21, self.localisation_21_fr, self.localisation_21_en = self.createLocalisationWithData(
            parent=self.localisation_2,
            order=1,
            name="Localisation 21",
            resume="Localisation 21"
        )

        self.localisation_1, self.localisation_1_fr, self.localisation_1_en = self.createLocalisationWithData(
            parent=None,
            order=1,
            name="Localisation 1",
            resume="Localisation 1"
        )
        self.localisation_12, self.localisation_12_fr, self.localisation_12_en = self.createLocalisationWithData(
            parent=self.localisation_1,
            order=2,
            name="Localisation 12",
            resume="Localisation 12"
        )
        self.localisation_11, self.localisation_11_fr, self.localisation_11_en = self.createLocalisationWithData(
            parent=self.localisation_1,
            order=1,
            name="Localisation 11",
            resume="Localisation 11"
        )
        self.localisation_112, self.localisation_112_fr, self.localisation_112_en = self.createLocalisationWithData(
            parent=self.localisation_11,
            order=2,
            name="Localisation 112",
            resume="Localisation 112"
        )
        self.localisation_111, self.localisation_111_fr, self.localisation_111_en = self.createLocalisationWithData(
            parent=self.localisation_11,
            order=1,
            name="Localisation 111",
            resume="Localisation 111"
        )

        # Check creation
        self.localisation_total = 8
        self.assertEqual(Localisation.objects.all().count(), self.localisation_total)
        self.assertEqual(LocalisationData.objects.all().count(), self.localisation_total*2)



    def test_get_all_localisation_in_order(self):
        # Create random localisation
        self.initLocalisationWithDataForTest()

        # Validate function
        localisation_list = get_all_model_in_order(model=Localisation)
        self.assertEqual(len(localisation_list), self.localisation_total)
        for i, localisation in enumerate(localisation_list):
            if i==0:
                self.assertEqual(localisation, self.localisation_1.pk)
            if i==1:
                self.assertEqual(localisation, self.localisation_11.pk)
            if i==2:
                self.assertEqual(localisation, self.localisation_111.pk)
            if i==3:
                self.assertEqual(localisation, self.localisation_112.pk)
            if i==4:
                self.assertEqual(localisation, self.localisation_12.pk)
            if i==5:
                self.assertEqual(localisation, self.localisation_2.pk)
            if i==6:
                self.assertEqual(localisation, self.localisation_21.pk)
            if i==7:
                self.assertEqual(localisation, self.localisation_22.pk)

    def test_get_all_localisationWithData_in_order(self):
        # Create random localisation
        self.initLocalisationWithDataForTest()

        # Validate function
        localisation_map_fr = get_all_modelWithData_in_order(
            model=Localisation,
            language=LanguageAvailable.FR.value
        )
        localisation_map_en = get_all_modelWithData_in_order(
            model=Localisation,
            language=LanguageAvailable.EN.value
        )
        self.assertEqual(len(localisation_map_fr), self.localisation_total)
        self.assertEqual(len(localisation_map_en), self.localisation_total)

        for i, localisation in enumerate(localisation_map_fr):
            if i==0:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_1_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_1_en)
            if i==1:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_11_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_11_en)
            if i==2:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_111_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_111_en)
            if i==3:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_112_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_112_en)
            if i==4:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_12_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_12_en)
            if i==5:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_2_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_2_en)
            if i==6:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_21_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_21_en)
            if i==7:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_22_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_22_en)

    def test_get_all_localisationDataWithPosition_in_order(self):
        # Create random localisation
        self.initLocalisationWithDataForTest()

        # Validate function
        localisation_map_fr = get_all_modelDataWithPosition_in_order(
            model=Localisation,
            language=LanguageAvailable.FR.value
        )
        localisation_map_en = get_all_modelDataWithPosition_in_order(
            model=Localisation,
            language=LanguageAvailable.EN.value
        )
        self.assertEqual(len(localisation_map_fr), self.localisation_total)

        for i, localisation in enumerate(localisation_map_fr):
            if i==0:
                self.assertEqual(localisation, self.localisation_1)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_1_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_1_en)
                self.assertEqual(localisation_map_fr[localisation][1], 0)
                self.assertEqual(localisation_map_en[localisation][1], 0)
            if i==1:
                self.assertEqual(localisation, self.localisation_11)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_11_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_11_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)
            if i==2:
                self.assertEqual(localisation, self.localisation_111)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_111_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_111_en)
                self.assertEqual(localisation_map_fr[localisation][1], 2)
                self.assertEqual(localisation_map_en[localisation][1], 2)
            if i==3:
                self.assertEqual(localisation, self.localisation_112)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_112_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_112_en)
                self.assertEqual(localisation_map_fr[localisation][1], 2)
                self.assertEqual(localisation_map_en[localisation][1], 2)
            if i==4:
                self.assertEqual(localisation, self.localisation_12)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_12_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_12_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)
            if i==5:
                self.assertEqual(localisation, self.localisation_2)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_2_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_2_en)
                self.assertEqual(localisation_map_fr[localisation][1], 0)
                self.assertEqual(localisation_map_en[localisation][1], 0)
            if i==6:
                self.assertEqual(localisation, self.localisation_21)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_21_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_21_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)
            if i==7:
                self.assertEqual(localisation, self.localisation_22)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_22_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_22_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)

