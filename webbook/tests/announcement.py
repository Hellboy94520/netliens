from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Library to create and use an image
from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from webbook.models import Announcement, AnnouncementStats, User, Category, Localisation
from webbook.forms import AnnouncementUserForm

class AnnouncementModelTestCase(TestCase):
    def setUp(self):
        self.title = "This is a title !"
        self.content = "This is an announcement !"
        im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
        im_io = BytesIO() # a BytesIO object for saving image
        im.save(im_io, 'JPEG') # save the image to im_io
        im_io.seek(0) # seek to the beginning
        self.image_name="random-name.jpg"
        self.image = InMemoryUploadedFile(
            im_io, None, self.image_name, 'image/jpeg', len(im_io.getvalue()), None)
        self.website = "www.toto.fr"
        self.nl = 5
        self.owner = None
        self.is_enable = True
        self.is_valid = True

    def test_default_construction(self):
        l_announcement = Announcement()
        self.assertEqual(l_announcement.title, "", "[LOCAL] Title is not empty !")
        self.assertEqual(l_announcement.content, "", "[LOCAL] Content is not empty !")
        self.assertEqual(l_announcement.image.name, None, "[LOCAL] Image name is not empty !")
        self.assertEqual(l_announcement.website, "", "[LOCAL] Website is not empty !")
        self.assertEqual(l_announcement.nl, 0, "[LOCAL] NLLevel is not equal to 0 !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertFalse(l_announcement.is_enable, "[LOCAL] Is_Enable is not False !")
        self.assertFalse(l_announcement.is_valid, "[LOCAL] Is_Valid is not False !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()

    def test_default_construction_database(self):
        l_announcement = Announcement()
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.title, "", "[LOCAL] Title is not empty !")
        self.assertEqual(l_announcement.content, "", "[LOCAL] Content is not empty !")
        self.assertEqual(l_announcement.image.name, "", "[LOCAL] Image name is not empty !")
        self.assertEqual(l_announcement.website, "", "[LOCAL] Website is not empty !")
        self.assertEqual(l_announcement.nl, 0, "[LOCAL] NLLevel is not equal to 0 !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertFalse(l_announcement.is_enable, "[LOCAL] Is_Enable is not False !")
        self.assertFalse(l_announcement.is_valid, "[LOCAL] Is_Valid is not False !")
        self.assertEqual(l_announcement.get_statistics().announcement, l_announcement, "[DB] Stats is not link to Announcement !")

    def test_construction(self):
        l_announcement = Announcement(  title=self.title,
                                        content=self.content,
                                        image=self.image,
                                        website=self.website,
                                        nl=self.nl,
                                        is_enable=self.is_enable,
                                        is_valid=self.is_valid)
        self.assertEqual(l_announcement.title, self.title, "[LOCAL] Title is incorrect !")
        self.assertEqual(l_announcement.content, self.content, "[LOCAL] Content is incorrect !")
        self.assertEqual(l_announcement.image, self.image, "[LOCAL] Image name is incorrect !")
        self.assertEqual(l_announcement.website, self.website, "[LOCAL] Website incorrect !")
        self.assertEqual(l_announcement.nl, self.nl, "[LOCAL] NLLevel is incorrect !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertEqual(l_announcement.is_enable, self.is_enable, "[LOCAL] Is_Enable is not False !")
        self.assertEqual(l_announcement.is_valid, self.is_valid, "[LOCAL] Is_Valid is not False !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()

    def test_construction_with_owner(self):
        l_email = "toto@gmail.com"
        l_user = User.objects.create_user(email=l_email, password="tototiti")
        self.assertEqual(User.objects.all().count(), 1, "[LOCAL] User has not been created !")
        l_announcement = Announcement(owner = l_user)
        self.assertEqual(l_announcement.owner.email, l_email, "[LOCAL] Username is incorrect !")

    def test_construction_with_stats(self):
        l_announcement = Announcement(  title=self.title,
                                        content=self.content,
                                        image=self.image,
                                        website=self.website,
                                        nl=self.nl,
                                        is_enable=self.is_enable,
                                        is_valid=self.is_valid)
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()

    def test_construction_database(self):
        l_announcement = Announcement(  title=self.title,
                                        content=self.content,
                                        image=self.image,
                                        website=self.website,
                                        nl=self.nl,
                                        is_enable=self.is_enable,
                                        is_valid=self.is_valid)
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title, "[DB] Title is incorrect !")
        self.assertEqual(l_announcement.content, self.content, "[DB] Content is incorrect !")
        self.assertIsNotNone(l_announcement.image.name, "[DB] Image name is None !")
        self.assertEqual(l_announcement.website, self.website, "[DB] Website incorrect !")
        self.assertEqual(l_announcement.nl, self.nl, "[DB] NLLevel is incorrect !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertEqual(l_announcement.is_enable, self.is_enable, "[DB] Is_Enable is not False !")
        self.assertEqual(l_announcement.is_valid, self.is_valid, "[DB] Is_Valid is not False !")

    def test_construction_with_owner_database(self):
        l_email = "toto"
        l_user = User.objects.create_user(email=l_email, password="tototiti")
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_announcement = Announcement(owner = l_user)
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.owner.email, l_email, "[DB] Email is incorrect !")

    def test_construction_with_stats_database(self):
        l_announcement = Announcement()
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.get_statistics().announcement, l_announcement, "[DB] Stats is not link to Announcement !")
        l_announcement.delete()
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement has not been deleted !")
        self.assertEqual(AnnouncementStats.objects.all().count(), 0, "[DB] AnnouncementStats has not been deleted !")

class AnnouncementUserFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="toto@gmail.com", password="tototititutu")
        self.title = "This is a title !"
        self.content = "This is an announcement !"
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
        self.is_enable = False
        self.is_valid = False
        self.category = Category.objects.create(name="Category", resume="This is a category", is_enable=True)
        self.localisation = Localisation.objects.create(name="Localisation", resume="This is a localisation", is_enable=True)

    def test_valid(self):
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': self.website,
                'nl': 0,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid !")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title, "[DB] Title is incorrect !")
        self.assertEqual(l_announcement.content, self.content, "[DB] Content is incorrect !")
        self.assertIsNotNone(l_announcement.image, "[DB] Image name is not empty !")
        self.assertEqual(l_announcement.website, self.website, "[DB] Website incorrect !")
        self.assertEqual(l_announcement.nl, self.nl, "[DB] NLLevel is incorrect !")
        self.assertEqual(l_announcement.category, self.category, "[DB] Category is incorrect !")
        self.assertEqual(l_announcement.is_enable, self.is_enable, "[DB] is_enable incorrect !")
        self.assertEqual(l_announcement.is_valid, self.is_valid, "[DB] is_valid is incorrect !")

    def test_invalid_title(self):
        # Title empty
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': "",
                'content': self.content,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], "This field is required.", "Error message not expected !")
        # Title with spaces only
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': "   ",
                'content': self.content,
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], "This field is required.", "Error message not expected !")

    def test_invalid_content(self):
        # Content empty
        l_announcement = AnnouncementUserForm(
            user=self.user,data={'title': self.title,
                'content': "",
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['content'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['content'].errors[0], "This field is required.", "Error message not expected !")
        # Content with spaces only
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': "          ",
                'website': self.website,
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['content'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['content'].errors[0], "This field is required.", "Error message not expected !")

    def test_invalid_website(self):     
        # Website empty
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': "",
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "This field is required.", "Error message not expected !")
        # Website incorrect format
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': "toto",
                'nl': self.nl,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "Enter a valid URL.", "Error message not expected !")
        # Website incomplete format (default is http)
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
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

    def test_nl0(self):
        # test with only NL0 available (default)
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
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
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': self.website,
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
        self.user.nl1 = 1
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
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
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': self.website,
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
        self.user.nl1 = 1
        self.user.nl2 = 1
        self.user.nl3 = 1
        self.user.nl4 = 2
        self.user.nl5 = 1
        self.user.nl6 = 1
        self.user.nl7 = 1
        l_announcement = AnnouncementUserForm(
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': self.website,
                'nl': 4,
                'category': self.category.pk,
                'localisation': self.localisation.pk},
            files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), f"Form is not valid !")
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
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': self.website,
                'nl': 4,
                'category': self.category.pk,
                'localisation': self.localisation.pk})
        self.assertTrue(l_announcement.is_valid(), "Form is valid !")
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
            user=self.user,
            data={'title': self.title,
                'content': self.content,
                'website': self.website,
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

    def test_category(self):
        Category.objects.create(name="Toto Disabled", resume="This is toto category", is_enable=False)
        l_toto = Category.objects.create(name="Toto Enable", resume="This is toto category", is_enable=True)
        Category.objects.create(name="Toto Children 1 Enable", resume="This is sub-toto category", is_enable=True, parent=l_toto)
        Category.objects.create(name="Toto Children 2 Disabled", resume="This is sub-toto category", is_enable=False, parent=l_toto)
        self.assertEqual(Category.objects.all().count(), 5)
        l_announcement = AnnouncementUserForm(user=self.user)
        self.assertEqual(l_announcement.fields['category'].queryset.count(), 3)
        for l_category in l_announcement.fields['category'].queryset:
            self.assertTrue(l_category.is_enable, "Category is not enable !")

    def test_localisation(self):
        Localisation.objects.create(name="Toto Disabled", resume="This is toto localisation", is_enable=False)
        l_toto = Localisation.objects.create(name="Toto Enable", resume="This is toto localisation", is_enable=True)
        Localisation.objects.create(name="Toto Children 1 Enable", resume="This is sub-toto localisation", is_enable=True, parent=l_toto)
        Localisation.objects.create(name="Toto Children 2 Disabled", resume="This is sub-toto localisation", is_enable=False, parent=l_toto)
        self.assertEqual(Localisation.objects.all().count(), 5)
        l_announcement = AnnouncementUserForm(user=self.user)
        self.assertEqual(l_announcement.fields['localisation'].queryset.count(), 3)
        for l_localisation in l_announcement.fields['localisation'].queryset:
            self.assertTrue(l_localisation.is_enable, "Localisation is not enable !")
