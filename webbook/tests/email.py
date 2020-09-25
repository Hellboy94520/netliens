from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

from webbook.models import ActivationEmail
from webbook.forms import ActivationEmailForm

class ActivationEmailModelTestCase(TestCase):
    def test_minimal_construction(self):
        l_act_email = ActivationEmail()
        self.assertNotEqual(l_act_email.subject, "", "[LOCAL] subject is empty !")
        self.assertNotEqual(l_act_email.message, "", "[LOCAL] message is empty !")

    def test_minimal_construction_database(self):
        l_act_email = ActivationEmail()
        self.assertEqual(ActivationEmail.objects.all().count(), 0, "[DB] ActivationEmail already exist !")
        l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail has not been created !")
        self.assertNotEqual(l_act_email.subject, "", "[LOCAL] subject is empty !")
        self.assertNotEqual(l_act_email.message, "", "[LOCAL] message is empty !")

    def test_only_one_instance_can_be_save(self):
        l_act_email = ActivationEmail()
        self.assertEqual(ActivationEmail.objects.all().count(), 0, "[DB] ActivationEmail already exist !")
        l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail has not been created !")
        l_act_email = ActivationEmail()
        with self.assertRaises(ValidationError):
            l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] 2 ActivationEmail has been created !")

    def test_update_instance(self):
        l_act_email = ActivationEmail()
        self.assertEqual(ActivationEmail.objects.all().count(), 0, "[DB] ActivationEmail already exist !")
        l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail has not been created !")
        # Update object
        l_act_email = ActivationEmail.objects.filter()[0]
        l_subject = "This is a new subject !"
        l_act_email.subject = l_subject
        l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail instance is not unique !")
        # Test Subject
        l_act_email = ActivationEmail.objects.filter()[0]
        self.assertEqual(l_act_email.subject, l_subject, "[DB] Subject of ActivationEmail has not been update !")
        # Update object
        l_act_email = ActivationEmail.objects.filter()[0]
        l_message = "This is a new message !"
        l_act_email.message = l_message
        l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail instance is not unique !")
        # Test Subject
        l_act_email = ActivationEmail.objects.filter()[0]
        self.assertEqual(l_act_email.message, l_message, "[DB] Message of ActivationEmail has not been update !")

    def test_get_unexist_instance(self):
        self.assertEqual(ActivationEmail.objects.all().count(), 0, "[DB] ActivationEmail already exist !")
        l_act_email = ActivationEmail.objects.get_or_create(pk=0)
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail has not been created !")
        l_act_email = ActivationEmail.objects.get_or_create(pk=0)
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] Another ActivationEmail has been created !")


class ActivationEmailFormTestCase(TestCase):
    def setUp(self):
        self.subject = "This is a subject !"
        self.message = "This is a message !"

    def test_form_valid(self):
        l_act_email = ActivationEmailForm(data={'subject': self.subject, 
                                                'message': self.message})
        self.assertTrue(l_act_email.is_valid(), "Form is not valid !")
        self.assertEqual(ActivationEmail.objects.all().count(), 0, "[DB] ActivationEmail already exist !")
        l_act_email.save()
        self.assertEqual(ActivationEmail.objects.all().count(), 1, "[DB] ActivationEmail has not been created after save form !")
        l_act_email = ActivationEmail.objects.filter()[0]
        self.assertEqual(l_act_email.message, self.message, "[DB] subject invalid !")
        self.assertEqual(l_act_email.message, self.message, "[DB] message invalid !")

    def test_form_invalid(self):
        # Empty Subject
        l_act_email = ActivationEmailForm(data={'subject': "", 
                                                'message': self.message})
        self.assertFalse(l_act_email.is_valid(), "Form is valid !")
        self.assertEqual(len(l_act_email.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_act_email['subject'].errors), 1, "Expected only 1 error for 'subject' field !")
        self.assertEqual(l_act_email['subject'].errors[0], "This field is required.", "Error message not expected !")
        # Empty Message
        l_act_email = ActivationEmailForm(data={'subject': self.subject, 
                                                'message': ""})
        self.assertFalse(l_act_email.is_valid(), "Form is valid !")
        self.assertEqual(len(l_act_email.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_act_email['message'].errors), 1, "Expected only 1 error for 'message' field !")
        self.assertEqual(l_act_email['message'].errors[0], "This field is required.", "Error message not expected !")
        # Empty Subject and Message
        l_act_email = ActivationEmailForm(data={'subject': "", 
                                                'message': ""})
        self.assertFalse(l_act_email.is_valid(), "Form is valid !")
        self.assertEqual(len(l_act_email.errors), 2, "Expected only 2 errors !")
        self.assertEqual(len(l_act_email['subject'].errors), 1, "Expected only 1 error for 'subject' field !")
        self.assertEqual(l_act_email['subject'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_act_email['message'].errors), 1, "Expected only 1 error for 'message' field !")
        self.assertEqual(l_act_email['message'].errors[0], "This field is required.", "Error message not expected !")
