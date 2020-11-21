from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404

# Library to create and use an image
from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from webbook.models import LanguageAvailable, AnnouncementLanguage, Announcement, AnnouncementStats, TITLE_MAX_LENGTH, NAME_MAX_LENGTH
from webbook.models import User, Category, Localisation
from webbook.forms import AnnouncementLanguageForm, AnnouncementUserForm

class AnnouncementModelTestCase(TestCase):
    """ 
        -----------------------------------------
        AnnouncementModel tests
        -----------------------------------------
    """
    def setUp(self):
        # Variable for Announcement Model
        self.name = "toto"
        im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
        im_io = BytesIO() # a BytesIO object for saving image
        im.save(im_io, 'JPEG') # save the image to im_io
        im_io.seek(0) # seek to the beginning
        self.image_name="random-name.jpg"
        self.image = InMemoryUploadedFile(
            im_io, None, self.image_name, 'image/jpeg', len(im_io.getvalue()), None)
        self.website = "www.toto.fr"
        self.category = Category.objects.create(name="Category", resume="This is a category", is_enable=True)
        self.localisation = Localisation.objects.create(name="Localisation", resume="This is a localisation", is_enable=True)
        self.nl = 5
        self.owner = User.objects.create(email="toto@gmail.com", password="tititututoto")
        self.is_enable = True
        self.is_valid = True
        self.is_on_homepage = True

        # AnnouncementLanguage creation
        self.announcement_language_en = AnnouncementLanguage(
            title = "This is a Title !",
            content = "This is a content !",
            language = LanguageAvailable.EN.value)
        self.announcement_language_fr = AnnouncementLanguage(
            title = "C'est un Titre !",
            content = "C'est un contenue !",
            language = LanguageAvailable.FR.value)


    def test_default_construction(self):
        l_announcement = Announcement()
        self.assertEqual(l_announcement.name, "")
        self.assertEqual(l_announcement.image.name, None)
        self.assertEqual(l_announcement.website, "")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.category
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.localisation
        self.assertEqual(l_announcement.nl, 0)
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertFalse(l_announcement.is_enable)
        self.assertFalse(l_announcement.is_valid)
        self.assertFalse(l_announcement.is_on_homepage)
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()


    def test_construction(self):
        l_announcement = Announcement(
            name = self.name,
            image = self.image,
            website = self.website,
            category = self.category,
            localisation = self.localisation,
            nl = self.nl,
            owner = self.owner,
            is_enable = self.is_enable,
            is_valid = self.is_valid,
            is_on_homepage = self.is_on_homepage
        )
        self.assertEqual(l_announcement.name, self.name)
        self.assertEqual(l_announcement.image.name, self.image_name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()


    def test_default_construction_database(self):
        l_announcement = Announcement()
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.name, "")
        self.assertEqual(l_announcement.image.name, "")
        self.assertEqual(l_announcement.website, "")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.category
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.localisation
        self.assertEqual(l_announcement.nl, 0)
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertFalse(l_announcement.is_enable)
        self.assertFalse(l_announcement.is_valid)
        self.assertEqual(l_announcement.get_statistics().announcement, l_announcement, "[DB] Stats is not link to Announcement !")


    def test_construction_database(self):
        l_announcement = Announcement(
            name = self.name,
            image = self.image,
            website = self.website,
            category = self.category,
            localisation = self.localisation,
            nl = self.nl,
            owner = self.owner,
            is_enable = self.is_enable,
            is_valid = self.is_valid,
            is_on_homepage = self.is_on_homepage
        )
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.name, self.name)
        self.assertIsNotNone(l_announcement.image.name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)
        self.assertEqual(AnnouncementStats.objects.all().count(), 1, "[DB] AnnouncementStats has not been created in same time as Announcement!")


    def test_construction_database_with_one_language(self):
        l_announcement = Announcement(
            name = self.name,
            image = self.image,
            website = self.website,
            category = self.category,
            localisation = self.localisation,
            nl = self.nl,
            owner = self.owner,
            is_enable = self.is_enable,
            is_valid = self.is_valid,
            is_on_homepage = self.is_on_homepage
        )
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] AnnouncementLanguage already exist !")
        self.announcement_language_en.announcement = l_announcement
        self.announcement_language_en.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1, "[DB] AnnouncementLanguage has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.name, self.name)
        self.assertIsNotNone(l_announcement.image.name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)
        self.assertEqual(AnnouncementStats.objects.all().count(), 1, "[DB] AnnouncementStats has not been created in same time as Announcement!")


    def test_construction_database_with_two_languages(self):
        l_announcement = Announcement(
            name = self.name,
            image = self.image,
            website = self.website,
            category = self.category,
            localisation = self.localisation,
            nl = self.nl,
            owner = self.owner,
            is_enable = self.is_enable,
            is_valid = self.is_valid,
            is_on_homepage = self.is_on_homepage
        )
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] AnnouncementLanguage already exist !")
        self.announcement_language_en.announcement = l_announcement
        self.announcement_language_en.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1, "[DB] AnnouncementLanguage has not been created !")
        self.announcement_language_fr.announcement = l_announcement
        self.announcement_language_fr.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 2, "[DB] AnnouncementLanguage has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.name, self.name)
        self.assertIsNotNone(l_announcement.image.name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)
        self.assertEqual(AnnouncementStats.objects.all().count(), 1, "[DB] AnnouncementStats has not been created in same time as Announcement!")



class AnnouncementUserFormTestCase(TestCase):
    """ 
        -----------------------------------------
        AnnouncementUserForm tests
        -----------------------------------------
    """
    def setUp(self):
        self.name = "toto"
        im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
        im_io = BytesIO() # a BytesIO object for saving image
        im.save(im_io, 'JPEG') # save the image to im_io
        im_io.seek(0) # seek to the beginning
        self.image_name="random-name.jpg"
        self.image = InMemoryUploadedFile(
            im_io, None, self.image_name, 'image/jpeg', len(im_io.getvalue()), None
        )
        self.image_name_2="random-name-2.jpg"
        self.image_2 = InMemoryUploadedFile(
            im_io, None, self.image_name_2, 'image/jpeg', len(im_io.getvalue()), None
        )
        self.website = "http://www.toto.fr"
        self.nl = 0
        self.owner = User.objects.create(email="toto@gmail.com", password="tototititutu")
        self.is_enable = False
        self.is_valid = False
        self.is_on_homepage = False
        self.category = Category.objects.create(name="Category", resume="This is a category", order=1, is_enable=True)
        self.localisation = Localisation.objects.create(name="Localisation", resume="This is a localisation", order=1, is_enable=True)

    def test_valid(self):
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': 0,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.name, self.name)
        self.assertIsNotNone(l_announcement.image)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)

    def test_invalid_name(self):
        # Name empty
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': "",
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['name'].errors[0], "This field is required.", "Error message not expected !")

        # Max length
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': "s" * (NAME_MAX_LENGTH+1),
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['name'].errors[0], f"Ensure this value has at most {NAME_MAX_LENGTH} characters (it has {NAME_MAX_LENGTH+1}).", "Error message not expected !")

    def test_name_unique(self):
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': 0,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': f"{self.website}.com",
                'nl': 1,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, f"Expected only 1 error ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['name'].errors[0], f"Announcement with this Name already exists.", "Error message not expected !")

    def test_invalid_website(self):     
        # Website empty
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "This field is required.", "Error message not expected !")
        
        # Website incorrect format
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': "toto",
                'nl': 1,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "Enter a valid URL.", "Error message not expected !")
        
        # Website incomplete format (default is http)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': "toto.fr",
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.website, "http://toto.fr", "Incorrect website format !")

    def test_website_already_exist(self):
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': f"{self.name}_1",
                'website': self.website,
                'nl': 1,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        #INFO: Remove image because problem is generated
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, f"Expected only 1 error ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "Announcement with this Website already exists.", "Error message not expected !")

    def test_nl0(self):
        # test with only NL0 available (default)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': 0,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(l_announcement.cleaned_data['nl'], '0')
        self.assertTrue("<option value=\"0\" selected>0</option>" in str(l_announcement), "Select Option not found !")
        self.assertFalse("<option value=\"1\">1</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"2\">2</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"3\">3</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"4\">4</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"5\">5</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"6\">6</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"7\">7</option>" in str(l_announcement), "Option not expected !")
        l_announcement.save()

        # Test with no NLX available
        self.assertEqual(Announcement.objects.all().count(), 1)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': f"{self.name}_1",
                'website': f"{self.website}.com",
                'nl': 0,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertFalse("<option value=\"0\">0</option>" in str(l_announcement), "Select Option not found !")
        self.assertFalse("<option value=\"0\" selected>0</option>" in str(l_announcement), "Select Option not found !")
        self.assertFalse("<option value=\"1\">1</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"2\">2</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"3\">3</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"4\">4</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"5\">5</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"6\">6</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"7\">7</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1)
        self.assertEqual(len(l_announcement['nl'].errors), 1)
        self.assertEqual(l_announcement['nl'].errors[0], "Select a valid choice. 0 is not one of the available choices.")

    def test_nl1(self):
        # Test with only NL0 and NL1 available
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': 1,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid !")
        self.assertEqual(l_announcement.cleaned_data['nl'], '1')
        self.assertTrue("<option value=\"0\">0</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"1\" selected>1</option>" in str(l_announcement), "Select Option not found !")
        self.assertFalse("<option value=\"2\">2</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"3\">3</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"4\">4</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"5\">5</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"6\">6</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"7\">7</option>" in str(l_announcement), "Option not expected !")
        l_announcement.save()

        # Test with no NL1 available
        self.assertEqual(Announcement.objects.all().count(), 1)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': f"{self.name}_1",
                'website': f"{self.website}.com",
                'nl': 1,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue("<option value=\"0\">0</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"1\" selected>1</option>" in str(l_announcement), "Select Option found !")
        self.assertFalse("<option value=\"1\">1</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"2\">2</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"3\">3</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"4\">4</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"5\">5</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"6\">6</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse("<option value=\"7\">7</option>" in str(l_announcement), "Option not expected !")
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1)
        self.assertEqual(len(l_announcement['nl'].errors), 1)
        self.assertEqual(l_announcement['nl'].errors[0], "Select a valid choice. 1 is not one of the available choices.")

    def test_all_nl(self):
        # Test with all NL available
        self.owner.nl1 = 1
        self.owner.nl2 = 1
        self.owner.nl3 = 1
        self.owner.nl4 = 2
        self.owner.nl5 = 1
        self.owner.nl6 = 1
        self.owner.nl7 = 1
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': 4,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(l_announcement.cleaned_data['nl'], '4')
        self.assertTrue("<option value=\"0\">0</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"1\">1</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"2\">2</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"3\">3</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"4\" selected>4</option>" in str(l_announcement), "Select Option not found !")
        self.assertTrue("<option value=\"5\">5</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"6\">6</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"7\">7</option>" in str(l_announcement), "Option not found !")
        l_announcement.save()

        # Test with all NL available
        self.assertEqual(Announcement.objects.all().count(), 1)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': f"{self.name}_1",
                'website': f"{self.website}.com",
                'nl': 4,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(l_announcement.cleaned_data['nl'], '4')
        self.assertTrue("<option value=\"0\">0</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"1\">1</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"2\">2</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"3\">3</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"4\" selected>4</option>" in str(l_announcement), "Select Option not found !")
        self.assertTrue("<option value=\"5\">5</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"6\">6</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"7\">7</option>" in str(l_announcement), "Option not found !")
        l_announcement.save()

        # Test without NL4 available
        self.assertEqual(Announcement.objects.all().count(), 2)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': f"{self.name}_2",
                'website': f"{self.website}.net",
                'nl': 4,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue("<option value=\"0\">0</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"1\">1</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"2\">2</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"3\">3</option>" in str(l_announcement), "Option not found !")
        self.assertFalse("<option value=\"4\">4</option>" in str(l_announcement), "Select Option found !")
        self.assertFalse("<option value=\"4\" selected>4</option>" in str(l_announcement), "Option found !")
        self.assertTrue("<option value=\"5\">5</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"6\">6</option>" in str(l_announcement), "Option not found !")
        self.assertTrue("<option value=\"7\">7</option>" in str(l_announcement), "Option not found !")
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1)
        self.assertEqual(len(l_announcement['nl'].errors), 1)
        self.assertEqual(l_announcement['nl'].errors[0], "Select a valid choice. 4 is not one of the available choices.")

    def test_only_category_enabled(self):
        """
            Test if category disabled are not display
        """
        Category.objects.create(name="Category Disabled", resume="This is toto category", is_enable=False)
        l_toto = Category.objects.create(name="Category Enable", resume="This is toto category", is_enable=True)
        Category.objects.create(name="Category-Children 1 Enable", resume="This is sub-toto category", is_enable=True, parent=l_toto)
        Category.objects.create(name="Category-Children 2 Disabled", resume="This is sub-toto category", is_enable=False, parent=l_toto)
        self.assertEqual(Category.objects.all().count(), 5)
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertEqual(len(l_announcement.fields['category'].choices), 3)
        category_self = False
        category_enable = False
        category_children_enable = False
        for l_key, l_category in l_announcement.fields['category'].choices:
            self.assertTrue(l_category.is_enable, "Category is not enable !")
            if l_category.name not in (self.category.name, "Category Enable", "Category-Children 1 Enable"):
                self.assertTrue(False, "Category name does not expected !")

    def test_category_order(self):
        """
            Test if category are show in right order
                Category
                Category 1
                    Category-Children 1
                    Category-Children 2
                Category 2
                    Category-Children 1
                    Category-Children 2
        """
        l_category_1 = Category.objects.create(name="Category 1", order=2, resume="This is toto category", is_enable=True)
        l_category_2 = Category.objects.create(name="Category 2", order=3, resume="This is toto category", is_enable=True)
        Category.objects.create(name="Category-Children 2", order=2, resume="This is sub-toto category", is_enable=True, parent=l_category_2)
        Category.objects.create(name="Category-Children 1", order=1, resume="This is sub-toto category", is_enable=True, parent=l_category_2)
        Category.objects.create(name="Category-Children 1", order=1, resume="This is sub-toto category", is_enable=True, parent=l_category_1)
        Category.objects.create(name="Category-Children 2", order=2, resume="This is sub-toto category", is_enable=True, parent=l_category_1)
        self.assertEqual(Category.objects.all().count(), 7)

        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertEqual(len(l_announcement.fields['category'].choices), 7)
        self.assertEqual(len(l_announcement.fields['localisation'].choices), 1)
        l_category_choices = l_announcement.fields['category'].choices
        self.assertEqual(l_category_choices[0][1].name, "Category")
        self.assertEqual(l_category_choices[1][1].name, "Category 1")
        self.assertEqual(l_category_choices[2][1].name, "Category-Children 1")
        self.assertEqual(l_category_choices[3][1].name, "Category-Children 2")
        self.assertEqual(l_category_choices[4][1].name, "Category 2")
        self.assertEqual(l_category_choices[5][1].name, "Category-Children 1")
        self.assertEqual(l_category_choices[6][1].name, "Category-Children 2")


    def test_category_not_exist(self):
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': 2,
                'localisation': self.localisation.pk})
        self.assertFalse(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement.errors), 1, f"{l_announcement.errors}")
        self.assertEqual(len(l_announcement['category'].errors), 1)
        self.assertEqual(l_announcement['category'].errors[0], "Select a valid choice. 2 is not one of the available choices.")


    def test_category_deleted_between_valid_and_save(self):
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.category.delete()
        with self.assertRaises(Http404):
            l_announcement.save()
        self.assertEqual(Category.objects.all().count(), 0)


    def test_localisation_order(self):
        """
            Test if localisation are show in right order
                Localisation
                Localisation 1
                    Localisation-Children 1
                    Localisation-Children 2
                Localisation 2
                    Localisation-Children 1
                    Localisation-Children 2
        """
        l_localisation_1 = Localisation.objects.create(name="Localisation 1", order=2, resume="This is toto localisation", is_enable=True)
        l_localisation_2 = Localisation.objects.create(name="Localisation 2", order=3, resume="This is toto localisation", is_enable=True)
        Localisation.objects.create(name="Localisation-Children 2", order=2, resume="This is sub-toto localisation", is_enable=True, parent=l_localisation_2)
        Localisation.objects.create(name="Localisation-Children 1", order=1, resume="This is sub-toto localisation", is_enable=True, parent=l_localisation_2)
        Localisation.objects.create(name="Localisation-Children 1", order=1, resume="This is sub-toto localisation", is_enable=True, parent=l_localisation_1)
        Localisation.objects.create(name="Localisation-Children 2", order=2, resume="This is sub-toto localisation", is_enable=True, parent=l_localisation_1)
        self.assertEqual(Localisation.objects.all().count(), 7)

        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': 3,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertEqual(len(l_announcement.fields['category'].choices), 1)
        self.assertEqual(len(l_announcement.fields['localisation'].choices), 7)
        l_localisation_choices = l_announcement.fields['localisation'].choices
        self.assertEqual(l_localisation_choices[0][1].name, "Localisation")
        self.assertEqual(l_localisation_choices[1][1].name, "Localisation 1")
        self.assertEqual(l_localisation_choices[2][1].name, "Localisation-Children 1")
        self.assertEqual(l_localisation_choices[3][1].name, "Localisation-Children 2")
        self.assertEqual(l_localisation_choices[4][1].name, "Localisation 2")
        self.assertEqual(l_localisation_choices[5][1].name, "Localisation-Children 1")
        self.assertEqual(l_localisation_choices[6][1].name, "Localisation-Children 2")


    def test_localisation_not_exist(self):
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': 2})
        self.assertFalse(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement.errors), 1, f"{l_announcement.errors}")
        self.assertEqual(len(l_announcement['localisation'].errors), 1)
        self.assertEqual(l_announcement['localisation'].errors[0], "Select a valid choice. 2 is not one of the available choices.")


    def test_localisation_deleted_between_valid_and_save(self):
        l_announcement = AnnouncementUserForm(
            user=self.owner,
            data={'name': self.name,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.localisation.delete()
        with self.assertRaises(Http404):
            l_announcement.save()
        self.assertEqual(Localisation.objects.all().count(), 0)


class AnnouncementLanguageModelTestCase(TestCase):
    """ 
        -----------------------------------------
        AnnouncementLanguageModel tests
        -----------------------------------------
    """
    def setUp(self):
        self.title_en = "It is a title !"
        self.content_en = "This is announcement !"
        self.language_en = LanguageAvailable.EN.value

        self.title_fr = "C'est un titre !"
        self.content_fr = "C'est une annonce !"
        self.language_fr = LanguageAvailable.FR.value

        self.announcement = Announcement.objects.create()


    def test_default_construction(self):
        l_announcement_language = AnnouncementLanguage()
        self.assertEqual(l_announcement_language.title, "")
        self.assertEqual(l_announcement_language.content, "")
        self.assertEqual(l_announcement_language.language, "")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement_language.announcement


    def test_construction(self):
        l_announcement_language = AnnouncementLanguage(
            title = self.title_en,
            content = self.content_en,
            language = self.language_en,
            announcement = self.announcement)
        self.assertEqual(l_announcement_language.title, self.title_en)
        self.assertEqual(l_announcement_language.content, self.content_en)
        self.assertEqual(l_announcement_language.language, self.language_en)
        self.assertEqual(l_announcement_language.announcement, self.announcement)


    def test_default_construction_database(self):
        l_announcement_language = AnnouncementLanguage()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0)
        l_announcement_language.save()
        l_announcement_language = AnnouncementLanguage.objects.all()[0]
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1)
        self.assertEqual(l_announcement_language.title, "")
        self.assertEqual(l_announcement_language.content, "")
        self.assertEqual(l_announcement_language.language, "")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement_language.announcement


    def test_default_construction_database(self):
        l_announcement_language = AnnouncementLanguage(
            title = self.title_en,
            content = self.content_en,
            language = self.language_en,
            announcement = self.announcement)
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0)
        l_announcement_language.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1)
        l_announcement_language = AnnouncementLanguage.objects.all()[0]
        self.assertEqual(l_announcement_language.title, self.title_en)
        self.assertEqual(l_announcement_language.content, self.content_en)
        self.assertEqual(l_announcement_language.language, self.language_en)
        self.assertEqual(l_announcement_language.announcement, self.announcement)



class AnnouncementLanguageFormTestCase(TestCase):
    """ 
        -----------------------------------------
        AnnouncementLanguageForm tests
        -----------------------------------------
    """
    def setUp(self):
        self.title_en = "This is a title !"
        self.content_en = "This is announcement !"
        self.language_en = LanguageAvailable.EN.value

        self.title_fr = "C'est un titre !"
        self.content_fr = "C'est une annonce !"
        self.language_fr = LanguageAvailable.FR.value

        self.announcement = Announcement.objects.create()


    def test_valid_en(self):
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_en,
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_announcement.is_valid(self.announcement), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        l_announcement.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1, "[DB] AnnouncementLanguage has not been created after save form !")
        l_announcement = AnnouncementLanguage.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title_en)
        self.assertEqual(l_announcement.content, self.content_en)
        self.assertEqual(l_announcement.language, self.language_en)


    def test_valid_fr(self):
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_fr,
                'content': self.content_fr,
                'language': self.language_fr
            }
        )
        self.assertTrue(l_announcement.is_valid(self.announcement), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        l_announcement.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1, "[DB] AnnouncementLanguage has not been created after save form !")
        l_announcement = AnnouncementLanguage.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title_fr)
        self.assertEqual(l_announcement.content, self.content_fr)
        self.assertEqual(l_announcement.language, self.language_fr)


    def test_title(self):
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        # Empty Title
        l_announcement = AnnouncementLanguageForm(
            data={'title': "",
                'content': self.content_fr,
                'language': self.language_fr
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], "This field is required.", "Error message not expected !")

        # Title too large
        l_announcement = AnnouncementLanguageForm(
            data={'title': "s" * (TITLE_MAX_LENGTH+1),
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], f"Ensure this value has at most {TITLE_MAX_LENGTH} characters (it has {TITLE_MAX_LENGTH+1}).", "Error message not expected !")

    def test_content(self):
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        # Empty Title
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_fr,
                'content': "",
                'language': self.language_fr
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['content'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['content'].errors[0], "This field is required.", "Error message not expected !")


    def test_language(self):
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        # Empty Language
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_fr,
                'content': self.content_fr,
                'language': ""
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['language'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['language'].errors[0], "This field is required.", "Error message not expected !")

        # Invalid Language value
        l_language = "ZZ"
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_fr,
                'content': self.content_fr,
                'language': l_language
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['language'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['language'].errors[0], f"Select a valid choice. {l_language} is not one of the available choices.", "Error message not expected !")


    def test_language_already_exist(self):
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        # Generate an English Language valid
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_en,
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_announcement.is_valid(self.announcement), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 0, "[DB] an AnnouncementLanguage already exist !")
        l_announcement.save()
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1, "[DB] AnnouncementLanguage has not been created after save form !")
        # English Language already exist
        l_announcement = AnnouncementLanguageForm(
            data={'title': self.title_en,
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementLanguage.objects.all().count(), 1, "[DB] AnnouncementLanguage has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['language'].errors), 1, "Expected only 1 error for 'language' field !")
        self.assertEqual(l_announcement['language'].errors[0], f"This Language already exist for this announcement !")

