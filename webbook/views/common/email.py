from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site

#TODO: Get it from settings
EMAIL_FROM = "noreply@netliens.com"

def send_mail(request,
        subject_template_name: str,
        email_template_name: str,
        context: list,
        to_email: list):
    """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    # Prepare information
    l_current_site = get_current_site(request)
    l_context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': l_current_site.domain,
        'site_name': l_current_site.name,
        **context
    }

    # Send Email
    subject = loader.render_to_string(subject_template_name, l_context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, l_context)
    email_message = EmailMultiAlternatives(subject, body, EMAIL_FROM, to_email)
    email_message.send()

