from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.conf import settings

# Library to create and use an image
from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from webbook.models import LanguageAvailable, AnnouncementData, Announcement, AnnouncementStats, TITLE_MAX_LENGTH, URL_MAX_LENGTH
from webbook.views.account import AnnouncementCreationView
from webbook.models import User, Category, CategoryData, Localisation
from webbook.forms import AnnouncementUserSettingForm, AnnouncementUserDataForm

class AnnouncementModelTestCase(TestCase):
    """
        -----------------------------------------
        AnnouncementModel tests
        -----------------------------------------
    """
    def setUp(self):
        # Variable for Announcement Model
        self.url = "toto"
        im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
        im_io = BytesIO() # a BytesIO object for saving image
        im.save(im_io, 'JPEG') # save the image to im_io
        im_io.seek(0) # seek to the beginning
        self.image_name="random-name.jpg"
        self.image = InMemoryUploadedFile(
            im_io, None, self.image_name, 'image/jpeg', len(im_io.getvalue()), None)
        self.website = "www.toto.fr"
        self.category = Category.objects.create(is_enable=True)
        self.localisation = Localisation.objects.create(code="ABC", is_enable=True)
        self.nl = 5
        self.owner = User.objects.create(email="toto@gmail.com", password="tititututoto")
        self.is_enable = True
        self.is_valid = True
        self.is_on_homepage = True

        # AnnouncementData creation
        self.announcement_language_en = AnnouncementData(
            title = "This is a Title !",
            content = "This is a content !",
            language = LanguageAvailable.EN.value)
        self.announcement_language_fr = AnnouncementData(
            title = "C'est un Titre !",
            content = "C'est un contenue !",
            language = LanguageAvailable.FR.value)


    def test_default_construction(self):
        l_announcement = Announcement()
        self.assertEqual(l_announcement.url, "")
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
            url = self.url,
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
        self.assertEqual(l_announcement.url, self.url)
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
        l_announcement = Announcement(
            category=self.category,
            localisation=self.localisation,
            owner=self.owner)
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.url, "")
        self.assertEqual(l_announcement.image.name, "")
        self.assertEqual(l_announcement.website, "")
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, 0)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertFalse(l_announcement.is_enable)
        self.assertFalse(l_announcement.is_valid)


    def test_construction_database(self):
        l_announcement = Announcement(
            url = self.url,
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
        self.assertEqual(l_announcement.url, self.url)
        self.assertIsNotNone(l_announcement.image.name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)


    def test_construction_database_with_one_language(self):
        l_announcement = Announcement(
            url = self.url,
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
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] AnnouncementData already exist !")
        self.announcement_language_en.announcement = l_announcement
        self.announcement_language_en.save()
        self.assertEqual(AnnouncementData.objects.all().count(), 1, "[DB] AnnouncementData has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.url, self.url)
        self.assertIsNotNone(l_announcement.image.name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)


    def test_construction_database_with_two_languages(self):
        l_announcement = Announcement(
            url = self.url,
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
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] AnnouncementData already exist !")
        self.announcement_language_en.announcement = l_announcement
        self.announcement_language_en.save()
        self.assertEqual(AnnouncementData.objects.all().count(), 1, "[DB] AnnouncementData has not been created !")
        self.announcement_language_fr.announcement = l_announcement
        self.announcement_language_fr.save()
        self.assertEqual(AnnouncementData.objects.all().count(), 2, "[DB] AnnouncementData has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.url, self.url)
        self.assertIsNotNone(l_announcement.image.name)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)


    def test_category_inherit_in_announcement(self):
        # Create Children category
        category_children = Category.objects.create(parent=self.category, is_enable=True)
        self.assertEqual(Category.objects.all().count(), 2)

        # Create Announcement and check data
        l_object = Announcement.objects.create(
            url = self.url,
            image = self.image,
            website = self.website,
            category = category_children,
            localisation = self.localisation,
            nl = self.nl,
            owner = self.owner,
            is_enable = self.is_enable,
            is_valid = self.is_valid,
            is_on_homepage = self.is_on_homepage
        )
        self.assertEqual(Announcement.objects.all().count(), 1)
        self.assertEqual(l_object.category, category_children)

        # Delete Category associated to this announcement
        category_children.delete()

        # Update Announcement and check new category
        l_object = Announcement.objects.get(pk=l_object.pk)
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Localisation.objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(l_object.category, self.category)
        self.assertEqual(l_object.localisation, self.localisation)
        self.assertEqual(l_object.owner, self.owner)

class AnnouncementUserSettingFormTestCase(TestCase):
    """
        -----------------------------------------
        AnnouncementUserSettingFormTestCase tests
        -----------------------------------------
    """
    def setUp(self):
        self.url = "toto"
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
        self.category = Category.objects.create(order=1, is_enable=True)
        self.localisation = Localisation.objects.create(code="ABC", order=1, is_enable=True)

    def test_valid(self):
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk,},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.url, self.url)
        self.assertIsNotNone(l_announcement.image)
        self.assertEqual(l_announcement.website, self.website)
        self.assertEqual(l_announcement.category, self.category)
        self.assertEqual(l_announcement.localisation, self.localisation)
        self.assertEqual(l_announcement.nl, self.nl)
        self.assertEqual(l_announcement.owner, self.owner)
        self.assertEqual(l_announcement.is_enable, self.is_enable)
        self.assertEqual(l_announcement.is_valid, self.is_valid)
        self.assertEqual(l_announcement.is_on_homepage, self.is_on_homepage)

    def test_invalid_url(self):
        # Url empty
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': "",
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['url'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['url'].errors[0], "This field is required.", "Error message not expected !")

        # Max length
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': "s" * (URL_MAX_LENGTH+1),
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['url'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['url'].errors[0], f"Ensure this value has at most {URL_MAX_LENGTH} characters (it has {URL_MAX_LENGTH+1}).", "Error message not expected !")

        # Invalid character
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': "toto!",
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['url'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['url'].errors[0], f"Only alphanumeric characters are allowed.", "Error message not expected !")

    def test_url_unique(self):
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': 0,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': f"{self.website}.com",
                'nl': 1,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertFalse(l_announcement.is_valid(), f"Form is valid ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement.errors), 1, f"Expected only 1 error ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement['url'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_announcement['url'].errors[0], f"Announcement with this Url already exists.", "Error message not expected !")

    def test_invalid_website(self):
        # Website empty
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "This field is required.", "Error message not expected !")

        # Website incorrect format
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
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
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': "toto.fr",
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.website, "http://toto.fr", "Incorrect website format !")

    def test_website_already_exist(self):
        self.owner.nl1 = 1
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': f"{self.url}1",
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
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
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
        l_announcement.save(user=self.owner)

        # Test with no NLX available
        self.assertEqual(Announcement.objects.all().count(), 1)
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': f"{self.url}1",
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
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
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
        l_announcement.save(user=self.owner)

        # Test with no NL1 available
        self.assertEqual(Announcement.objects.all().count(), 1)
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': f"{self.url}1",
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
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
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
        l_announcement.save(user=self.owner)

        # Test with all NL available
        self.assertEqual(Announcement.objects.all().count(), 1)
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': f"{self.url}1",
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
        l_announcement.save(user=self.owner)

        # Test without NL4 available
        self.assertEqual(Announcement.objects.all().count(), 2)
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': f"{self.url}2",
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
        l_category_disabled = Category.objects.create(is_enable=False, order=2)
        l_category_enabled = Category.objects.create(is_enable=True, order=3)
        l_category_11 = Category.objects.create(is_enable=True, parent=l_category_enabled, order=1)
        l_category_12 = Category.objects.create(is_enable=False, parent=l_category_enabled, order=2)
        self.assertEqual(Category.objects.all().count(), 5)
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
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
        l_category_1 = Category.objects.create(order=2, is_enable=True)
        l_category_2 = Category.objects.create(order=3, is_enable=True)
        l_category_22 = Category.objects.create(order=2, is_enable=True, parent=l_category_2)
        l_category_21 = Category.objects.create(order=1, is_enable=True, parent=l_category_2)
        l_category_11 = Category.objects.create(order=1, is_enable=True, parent=l_category_1)
        l_category_12 = Category.objects.create(order=2, is_enable=True, parent=l_category_1)
        self.assertEqual(Category.objects.all().count(), 7)

        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertEqual(len(l_announcement.fields['category'].choices), 7)
        self.assertEqual(len(l_announcement.fields['localisation'].choices), 1)
        l_category_choices = l_announcement.fields['category'].choices
        self.assertEqual(l_category_choices[0][1], self.category)
        self.assertEqual(l_category_choices[1][1], l_category_1)
        self.assertEqual(l_category_choices[2][1], l_category_11)
        self.assertEqual(l_category_choices[3][1], l_category_12)
        self.assertEqual(l_category_choices[4][1], l_category_2)
        self.assertEqual(l_category_choices[5][1], l_category_21)
        self.assertEqual(l_category_choices[6][1], l_category_22)


    def test_category_not_exist(self):
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': 2,
                'localisation': self.localisation.pk})
        self.assertFalse(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement.errors), 1, f"{l_announcement.errors}")
        self.assertEqual(len(l_announcement['category'].errors), 1)
        self.assertEqual(l_announcement['category'].errors[0], "Select a valid choice. 2 is not one of the available choices.")


    def test_category_deleted_between_valid_and_save(self):
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.category.delete()
        with self.assertRaises(Http404):
            l_announcement.save(user=self.owner)
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
        l_localisation_1 = Localisation.objects.create(code="ABCA", order=2, is_enable=True)
        l_localisation_2 = Localisation.objects.create(code="ABCB", order=3, is_enable=True)
        l_localisation_22 = Localisation.objects.create(code="ABCC", order=2, is_enable=True, parent=l_localisation_2)
        l_localisation_21 = Localisation.objects.create(code="ABCD", order=1, is_enable=True, parent=l_localisation_2)
        l_localisation_11 = Localisation.objects.create(code="ABCE", order=1, is_enable=True, parent=l_localisation_1)
        l_localisation_12 = Localisation.objects.create(code="ABCF", order=2, is_enable=True, parent=l_localisation_1)
        self.assertEqual(Localisation.objects.all().count(), 7)

        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': 3,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertEqual(len(l_announcement.fields['category'].choices), 1)
        self.assertEqual(len(l_announcement.fields['localisation'].choices), 7)
        l_localisation_choices = l_announcement.fields['localisation'].choices
        self.assertEqual(l_localisation_choices[0][1], self.localisation)
        self.assertEqual(l_localisation_choices[1][1], l_localisation_1)
        self.assertEqual(l_localisation_choices[2][1], l_localisation_11)
        self.assertEqual(l_localisation_choices[3][1], l_localisation_12)
        self.assertEqual(l_localisation_choices[4][1], l_localisation_2)
        self.assertEqual(l_localisation_choices[5][1], l_localisation_21)
        self.assertEqual(l_localisation_choices[6][1], l_localisation_22)


    def test_localisation_not_exist(self):
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': 2})
        self.assertFalse(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(len(l_announcement.errors), 1, f"{l_announcement.errors}")
        self.assertEqual(len(l_announcement['localisation'].errors), 1)
        self.assertEqual(l_announcement['localisation'].errors[0], "Select a valid choice. 2 is not one of the available choices.")


    def test_localisation_deleted_between_valid_and_save(self):
        l_announcement = AnnouncementUserSettingForm(
            user=self.owner,
            data={'url': self.url,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid ! {l_announcement.errors}")
        self.localisation.delete()
        with self.assertRaises(Http404):
            l_announcement.save(user=self.owner)
        self.assertEqual(Localisation.objects.all().count(), 0)


class AnnouncementDataModelTestCase(TestCase):
    """
        -----------------------------------------
        AnnouncementDataModel tests
        -----------------------------------------
    """
    def setUp(self):
        self.title_en = "It is a title !"
        self.content_en = "This is announcement !"
        self.language_en = LanguageAvailable.EN.value

        self.title_fr = "C'est un titre !"
        self.content_fr = "C'est une annonce !"
        self.language_fr = LanguageAvailable.FR.value

        self.owner = User.objects.create(email="toto@gmail.com", password="tototititutu")
        self.category = Category.objects.create(order=1, is_enable=True)
        self.localisation = Localisation.objects.create(code="ABC", order=1, is_enable=True)

        self.announcement = Announcement.objects.create(
            category=self.category,
            localisation=self.localisation,
            owner=self.owner
        )

    def test_construction(self):
        l_announcement_language = AnnouncementData(
            title = self.title_en,
            content = self.content_en,
            language = self.language_en,
            announcement = self.announcement)
        self.assertEqual(l_announcement_language.title, self.title_en)
        self.assertEqual(l_announcement_language.content, self.content_en)
        self.assertEqual(l_announcement_language.language, self.language_en)
        self.assertEqual(l_announcement_language.announcement, self.announcement)


    def test_default_construction_database(self):
        l_announcement_language = AnnouncementData(
            title = self.title_en,
            content = self.content_en,
            language = self.language_en,
            announcement = self.announcement)
        self.assertEqual(AnnouncementData.objects.all().count(), 0)
        l_announcement_language.save()
        self.assertEqual(AnnouncementData.objects.all().count(), 1)
        l_announcement_language = AnnouncementData.objects.all()[0]
        self.assertEqual(l_announcement_language.title, self.title_en)
        self.assertEqual(l_announcement_language.content, self.content_en)
        self.assertEqual(l_announcement_language.language, self.language_en)
        self.assertEqual(l_announcement_language.announcement, self.announcement)


    def test_announcement_delete(self):
        # Create AnnouncementData associated to Category
        l_object = AnnouncementData.objects.create(
            title = self.title_en,
            content = self.content_en,
            language = self.language_en,
            announcement = self.announcement
        )
        self.assertEqual(AnnouncementData.objects.all().count(), 1)
        self.assertEqual(Announcement.objects.all().count(), 1)

        # Delete Category which delete CategoryData
        self.announcement.delete()
        self.assertEqual(Announcement.objects.all().count(), 0)
        self.assertEqual(AnnouncementData.objects.all().count(), 0)



class AnnouncementUserDataFormTestCase(TestCase):
    """
        -----------------------------------------
        AnnouncementUserDataFormTestCase tests
        -----------------------------------------
    """
    def setUp(self):
        self.title_en = "This is a title !"
        self.content_en = "This is announcement !"
        self.language_en = LanguageAvailable.EN.value

        self.title_fr = "C'est un titre !"
        self.content_fr = "C'est une annonce !"
        self.language_fr = LanguageAvailable.FR.value

        self.owner = User.objects.create(email="toto@gmail.com", password="tototititutu")
        self.category = Category.objects.create(order=1, is_enable=True)
        self.localisation = Localisation.objects.create(code="ABC", order=1, is_enable=True)

        self.announcement = Announcement.objects.create(
            category=self.category,
            localisation=self.localisation,
            owner=self.owner
        )


    def test_valid_en(self):
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_en,
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_announcement.is_valid(self.announcement), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(AnnouncementData.objects.all().count(), 1, "[DB] AnnouncementData has not been created after save form !")
        l_announcement = AnnouncementData.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title_en)
        self.assertEqual(l_announcement.content, self.content_en)
        self.assertEqual(l_announcement.language, self.language_en)


    def test_valid_fr(self):
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_fr,
                'content': self.content_fr,
                'language': self.language_fr
            }
        )
        self.assertTrue(l_announcement.is_valid(self.announcement), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(AnnouncementData.objects.all().count(), 1, "[DB] AnnouncementData has not been created after save form !")
        l_announcement = AnnouncementData.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title_fr)
        self.assertEqual(l_announcement.content, self.content_fr)
        self.assertEqual(l_announcement.language, self.language_fr)


    def test_title(self):
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        # Empty Title
        l_announcement = AnnouncementUserDataForm(
            data={'title': "",
                'content': self.content_fr,
                'language': self.language_fr
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], "This field is required.", "Error message not expected !")

        # Title too large
        l_announcement = AnnouncementUserDataForm(
            data={'title': "s" * (TITLE_MAX_LENGTH+1),
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], f"Ensure this value has at most {TITLE_MAX_LENGTH} characters (it has {TITLE_MAX_LENGTH+1}).", "Error message not expected !")

    def test_content(self):
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        # Empty Title
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_fr,
                'content': "",
                'language': self.language_fr
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['content'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['content'].errors[0], "This field is required.", "Error message not expected !")


    def test_language(self):
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        # Empty Language
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_fr,
                'content': self.content_fr,
                'language': ""
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['language'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['language'].errors[0], "This field is required.", "Error message not expected !")

        # Invalid Language value
        l_language = "ZZ"
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_fr,
                'content': self.content_fr,
                'language': l_language
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['language'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['language'].errors[0], f"Select a valid choice. {l_language} is not one of the available choices.", "Error message not expected !")


    def test_language_already_exist(self):
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        # Generate an English Language valid
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_en,
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_announcement.is_valid(self.announcement), f"Form is not valid ! {l_announcement.errors}")
        self.assertEqual(AnnouncementData.objects.all().count(), 0, "[DB] an AnnouncementData already exist !")
        l_announcement.save(user=self.owner)
        self.assertEqual(AnnouncementData.objects.all().count(), 1, "[DB] AnnouncementData has not been created after save form !")
        # English Language already exist
        l_announcement = AnnouncementUserDataForm(
            data={'title': self.title_en,
                'content': self.content_en,
                'language': self.language_en
            }
        )
        self.assertFalse(l_announcement.is_valid(self.announcement), f"Form is valid !")
        self.assertEqual(AnnouncementData.objects.all().count(), 1, "[DB] AnnouncementData has been created !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['language'].errors), 1, "Expected only 1 error for 'language' field !")
        self.assertEqual(l_announcement['language'].errors[0], f"This Language already exist for this announcement !")



class AnnouncementCreationView(TestCase):
    """
        -----------------------------------------
        AnnouncementCreationView tests
        -----------------------------------------
    """
    def setUp(self):
        self.email = "toto@gmail.com"
        self.email_2 = "titi.toto@gmail.com"
        self.password = "tititututoto"

        self.title_en = "This is a title !"
        self.content_en = "This is announcement !"
        self.language_en = LanguageAvailable.EN.value

        self.title_fr = "C'est un titre !"
        self.content_fr = "C'est une annonce !"
        self.language_fr = LanguageAvailable.FR.value

        self.url = "toto"
        im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
        im_io = BytesIO() # a BytesIO object for saving image
        im.save(im_io, 'JPEG') # save the image to im_io
        im_io.seek(0) # seek to the beginning
        self.image_name="random-name.jpg"
        self.image = InMemoryUploadedFile(
            im_io, None, self.image_name, 'image/jpeg', len(im_io.getvalue()), None)
        self.website = "http://www.toto.fr"
        self.category = Category.objects.create(is_enable=True)
        self.localisation = Localisation.objects.create(code="ABC", is_enable=True)
        self.nl = 0
        self.owner = User.objects.create_user(email=self.email, password=self.password, is_active=True)
        self.owner2 = User.objects.create_user(email=self.email_2, password=self.password, is_active=True)
        self.is_enable = True
        self.is_valid = True
        self.is_on_homepage = True


    def test_valid_only_english(self):
        """
            Test valid with English language
        """
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(Localisation.objects.all().count(), 1)

        # LoginView
        response = self.client.post(
            "/account/login/",
            { 'username': self.email,
              'password': self.password
            }
        )
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # Authentificate the user
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")

        # Create announcement settings
        response = self.client.post(
            "/account/announcement/creation/",
            { 'url': self.url,
              'website': self.website,
              'nl': self.nl,
              'category': self.category.pk,
              'localisation': self.localisation.pk,
            },
        )
        self.assertEqual(response.url, f"/account/announcement/{self.url}/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)

        # Create announcement data in english
        response = self.client.post(
            f"/account/announcement/{self.url}/",
            { 'title': self.title_en,
              'content': self.content_en,
              'language': self.language_en
            },
        )
        self.assertEqual(response.url, "/account/announcement/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)
        self.assertEqual(AnnouncementData.objects.all().count(), 1)


    def test_valid_only_french(self):
        """
            Test valid with French language
        """
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(Localisation.objects.all().count(), 1)

        # LoginView
        response = self.client.post(
            "/account/login/",
            { 'username': self.email,
              'password': self.password
            }
        )
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # Authentificate the user
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")

        # Create announcement settings
        response = self.client.post(
            "/account/announcement/creation/",
            { 'url': self.url,
              'website': self.website,
              'nl': self.nl,
              'category': self.category.pk,
              'localisation': self.localisation.pk,
            },
        )
        self.assertEqual(response.url, f"/account/announcement/{self.url}/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)

        # Create announcement data in english
        response = self.client.post(
            f"/account/announcement/{self.url}/",
            { 'title': self.title_fr,
              'content': self.content_fr,
              'language': self.language_fr
            },
        )
        self.assertEqual(response.url, "/account/announcement/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)
        self.assertEqual(AnnouncementData.objects.all().count(), 1)


    def test_valid_english_and_french(self):
        """
            Test valid with English and French languages
        """
        self.assertEqual(User.objects.all().count(), 2, "Model has not been created after submit valid form !")
        self.assertEqual(Category.objects.all().count(), 1, "Model has not been created after submit valid form !")
        self.assertEqual(Localisation.objects.all().count(), 1, "Model has not been created after submit valid form !")

        # LoginView
        response = self.client.post(
            "/account/login/",
            { 'username': self.email,
              'password': self.password
            }
        )
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # Authentificate the user
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")

        # Create announcement settings
        response = self.client.post(
            "/account/announcement/creation/",
            { 'url': self.url,
              'website': self.website,
              'nl': self.nl,
              'category': self.category.pk,
              'localisation': self.localisation.pk,
            },
        )
        self.assertEqual(response.url, f"/account/announcement/{self.url}/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)

        # Create announcement data in english
        response = self.client.post(
            f"/account/announcement/{self.url}/",
            { 'title': self.title_en,
              'content': self.content_en,
              'language': self.language_en
            },
        )
        self.assertEqual(response.url, "/account/announcement/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)
        self.assertEqual(AnnouncementData.objects.all().count(), 1)

        # Create announcement data in french
        response = self.client.post(
            f"/account/announcement/{self.url}/",
            { 'title': self.title_fr,
              'content': self.content_fr,
              'language': self.language_fr
            },
        )
        self.assertEqual(response.url, "/account/announcement/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)
        self.assertEqual(AnnouncementData.objects.all().count(), 2)


    def test_invalid_no_user_login(self):
        """
            Try to create an announcement anonymously
        """
        self.assertEqual(User.objects.all().count(), 2, "Model has not been created after submit valid form !")
        self.assertEqual(Category.objects.all().count(), 1, "Model has not been created after submit valid form !")
        self.assertEqual(Localisation.objects.all().count(), 1, "Model has not been created after submit valid form !")

        # Try to create announcement settings without login
        response = self.client.get("/account/announcement/creation/")
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next=/account/announcement/creation/", f"Response not expected : {response}")


    def test_invalid_user(self):
        """
            Try to add  a data to an announcement with another user
        """
        self.assertEqual(User.objects.all().count(), 2, "Model has not been created after submit valid form !")
        self.assertEqual(Category.objects.all().count(), 1, "Model has not been created after submit valid form !")
        self.assertEqual(Localisation.objects.all().count(), 1, "Model has not been created after submit valid form !")

        # LoginView (with first user)
        response = self.client.post(
            "/account/login/",
            { 'username': self.email,
              'password': self.password
            }
        )
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # Authentificate the user (with first user)
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")

        # Create announcement settings (with first user)
        response = self.client.post(
            "/account/announcement/creation/",
            { 'url': self.url,
              'website': self.website,
              'nl': self.nl,
              'category': self.category.pk,
              'localisation': self.localisation.pk,
            },
        )
        self.assertEqual(response.url, f"/account/announcement/{self.url}/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)

        # Logout (with first user)
        response = self.client.get("/account/logout/")
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # LoginView (with second user)
        response = self.client.post(
            "/account/login/",
            { 'username': self.email_2,
              'password': self.password
            }
        )
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # Authentificate the user (with second user)
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email_2, "Wrong user authentificated !")

        # Try to reach via get
        response = self.client.get(f"/account/announcement/{self.url}/")
        self.assertEqual(response.status_code, 404)

        # Try to reach via set
        response = self.client.post(
            f"/account/announcement/{self.url}/",
            { 'url': self.url,
              'website': self.website,
              'nl': self.nl,
              'category': self.category.pk,
              'localisation': self.localisation.pk,
            },
        )
        self.assertEqual(response.status_code, 404)


    def test_invalid_no_nl_available(self):
        """
            Try to create an announcement without nl available
        """
        self.assertEqual(User.objects.all().count(), 2, "Model has not been created after submit valid form !")
        self.assertEqual(Category.objects.all().count(), 1, "Model has not been created after submit valid form !")
        self.assertEqual(Localisation.objects.all().count(), 1, "Model has not been created after submit valid form !")

        # LoginView
        response = self.client.post(
            "/account/login/",
            { 'username': self.email,
              'password': self.password
            }
        )
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")

        # Authentificate the user
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")

        # Create a valid announcement settings
        response = self.client.post(
            "/account/announcement/creation/",
            { 'url': self.url,
              'website': self.website,
              'nl': self.nl,
              'category': self.category.pk,
              'localisation': self.localisation.pk,
            },
        )
        self.assertEqual(response.url, f"/account/announcement/{self.url}/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)

        # Try to create another announcement
        response = self.client.get("/account/announcement/creation/")
        self.assertEqual(response.url, f"/account/announcement/purchase/", f"Response not expected : {response}")
        self.assertEqual(Announcement.objects.all().count(), 1)
