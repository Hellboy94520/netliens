from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

# Library to create and use an image
from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from webbook.models import LanguageAvailable, AnnouncementData, Announcement
from webbook.models import User, Category, Localisation

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

