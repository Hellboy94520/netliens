from django.test import TestCase
from django.conf import settings

# Library to create and use an image
from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from webbook.models import LanguageAvailable, AnnouncementData, Announcement
from webbook.models import User, Category, CategoryData, Localisation

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
