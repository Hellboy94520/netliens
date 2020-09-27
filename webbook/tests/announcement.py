from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

# Library to create and use an image
from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from webbook.models import Announcement, AnnouncementStats, User
from webbook.forms import AnnouncementUserForm, AnnouncementAdminForm

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
            im_io, None, self.image_name, 'image/jpeg', len(im_io.getvalue()), None
        )
        self.website = "www.toto.fr"
        self.nllevel = 5
        self.owner = None
        self.is_enable = True
        self.is_valid = True

    def test_default_construction(self):
        l_announcement = Announcement()
        self.assertEqual(l_announcement.title, "", "[LOCAL] Title is not empty !")
        self.assertEqual(l_announcement.content, "", "[LOCAL] Content is not empty !")
        self.assertEqual(l_announcement.image.name, "", "[LOCAL] Image name is not empty !")
        self.assertEqual(l_announcement.website, "", "[LOCAL] Website is not empty !")
        self.assertEqual(l_announcement.nllevel, 0, "[LOCAL] NLLevel is not equal to 0 !")
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
        self.assertEqual(l_announcement.nllevel, 0, "[LOCAL] NLLevel is not equal to 0 !")
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
                                        nllevel=self.nllevel,
                                        is_enable=self.is_enable,
                                        is_valid=self.is_valid)
        self.assertEqual(l_announcement.title, self.title, "[LOCAL] Title is incorrect !")
        self.assertEqual(l_announcement.content, self.content, "[LOCAL] Content is incorrect !")
        self.assertEqual(l_announcement.image, self.image, "[LOCAL] Image name is incorrect !")
        self.assertEqual(l_announcement.website, self.website, "[LOCAL] Website incorrect !")
        self.assertEqual(l_announcement.nllevel, self.nllevel, "[LOCAL] NLLevel is incorrect !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertEqual(l_announcement.is_enable, self.is_enable, "[LOCAL] Is_Enable is not False !")
        self.assertEqual(l_announcement.is_valid, self.is_valid, "[LOCAL] Is_Valid is not False !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()

    def test_construction_with_owner(self):
        l_username = "toto"
        l_user = User.objects.create_user(username=l_username, password="tototiti")
        self.assertEqual(User.objects.all().count(), 1, "[LOCAL] User has not been created !")
        l_announcement = Announcement(owner = l_user)
        self.assertEqual(l_announcement.owner.username, l_username, "[LOCAL] Username is incorrect !")

    def test_construction_with_stats(self):
        l_announcement = Announcement(  title=self.title,
                                        content=self.content,
                                        image=self.image,
                                        website=self.website,
                                        nllevel=self.nllevel,
                                        is_enable=self.is_enable,
                                        is_valid=self.is_valid)
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.get_statistics()

    def test_construction_database(self):
        l_announcement = Announcement(  title=self.title,
                                        content=self.content,
                                        image=self.image,
                                        website=self.website,
                                        nllevel=self.nllevel,
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
        self.assertEqual(l_announcement.nllevel, self.nllevel, "[DB] NLLevel is incorrect !")
        with self.assertRaises(ObjectDoesNotExist):
            l_announcement.owner
        self.assertEqual(l_announcement.is_enable, self.is_enable, "[DB] Is_Enable is not False !")
        self.assertEqual(l_announcement.is_valid, self.is_valid, "[DB] Is_Valid is not False !")

    def test_construction_with_owner_database(self):
        l_username = "toto"
        l_user = User.objects.create_user(username=l_username, password="tototiti")
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_announcement = Announcement(owner = l_user)
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.owner.username, l_username, "[DB] Username is incorrect !")

    def test_construction_with_stats_database(self):
        l_announcement = Announcement()
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.get_statistics().announcement, l_announcement, "[DB] Stats is not link to Announcement !")

class AnnouncementUserFormTestCase(TestCase):
    def setUp(self):
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
        self.website = "http://www.toto.fr"
        self.nllevel = 5
        #TODO: Owner
        self.is_enable = False
        self.is_valid = False

    def test_valid(self):
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] an Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created after save form !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.title, self.title, "[DB] Title is incorrect !")
        self.assertEqual(l_announcement.content, self.content, "[DB] Content is incorrect !")
        self.assertIsNotNone(l_announcement.image, "[DB] Image name is not empty !")
        self.assertEqual(l_announcement.website, self.website, "[DB] Website incorrect !")
        self.assertEqual(l_announcement.nllevel, self.nllevel, "[DB] NLLevel is incorrect !")
        self.assertEqual(l_announcement.is_enable, self.is_enable, "[DB] is_enable incorrect !")
        self.assertEqual(l_announcement.is_valid, self.is_valid, "[DB] is_valid is incorrect !")

    def test_invalid(self):
        # Title empty
        l_announcement = AnnouncementUserForm(data={'title': "",
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], "This field is required.", "Error message not expected !")
        l_announcement = AnnouncementUserForm(data={'title': "   ",
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['title'].errors), 1, "Expected only 1 error for 'title' field !")
        self.assertEqual(l_announcement['title'].errors[0], "This field is required.", "Error message not expected !")
        # Content empty
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': "",
                                                    'website': self.website,
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['content'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['content'].errors[0], "This field is required.", "Error message not expected !")
        # Image empty
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': self.nllevel})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['image'].errors), 1, "Expected only 1 error for 'image' field !")
        self.assertEqual(l_announcement['image'].errors[0], "This field is required.", "Error message not expected !")

    def test_invalid_website(self):     
        # Website empty
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': "",
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "This field is required.", "Error message not expected !")
        # Website incorrect format
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': "toto",
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['website'].errors), 1, "Expected only 1 error for 'content' field !")
        self.assertEqual(l_announcement['website'].errors[0], "Enter a valid URL.", "Error message not expected !")
        # Website incomplete format (default is http)
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': "toto.fr",
                                                    'nllevel': self.nllevel},
                                              files={'image': self.image})
        self.assertTrue(l_announcement.is_valid(), "Form is valid !")
        self.assertEqual(Announcement.objects.all().count(), 0, "[DB] Announcement already exist !")
        l_announcement.save()
        self.assertEqual(Announcement.objects.all().count(), 1, "[DB] Announcement has not been created !")
        l_announcement = Announcement.objects.filter()[0]
        self.assertEqual(l_announcement.website, "http://toto.fr", "Incorrect website format !")

    def test_invalid_nllevel(self):
        # nllevel empty
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': ""},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['nllevel'].errors), 1, "Expected only 1 error for 'nllevel' field !")
        self.assertEqual(l_announcement['nllevel'].errors[0], "This field is required.", "Error message not expected !")
        # nllevel incorrect format
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': "toto"},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['nllevel'].errors), 1, "Expected only 1 error for 'nllevel' field !")
        self.assertEqual(l_announcement['nllevel'].errors[0], "Enter a whole number.", "Error message not expected !")
        # nllevel too small
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': -1},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['nllevel'].errors), 1, "Expected only 1 error for 'nllevel' field !")
        self.assertEqual(l_announcement['nllevel'].errors[0], "Ensure this value is greater than or equal to 0.", "Error message not expected !")
        # nllevel too high
        l_announcement = AnnouncementUserForm(data={'title': self.title,
                                                    'content': self.content,
                                                    'website': self.website,
                                                    'nllevel': 11},
                                              files={'image': self.image})
        self.assertFalse(l_announcement.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_announcement.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_announcement['nllevel'].errors), 1, "Expected only 1 error for 'nllevel' field !")
        self.assertEqual(l_announcement['nllevel'].errors[0], "Ensure this value is less than or equal to 10.", "Error message not expected !")
