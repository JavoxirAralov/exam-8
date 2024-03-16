from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from models import Product


def send_verification_email(email: str, _uuid: str):
    link = f'http://localhost:8000/api/v1/users/confirm-email/{_uuid}'

    context = {
        'link': link
    }

    html_message = render_to_string('', context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject='Emile saytdan ruyxatdan otdiz',
        body=plain_message,
        to=[email]
    )
    message.attach_alternative(html_message, '')
    message.send()


class Command(BaseCommand):
    help = "bugun bizda yangi productlar qo'shilsin"

    def handle(self, *args, **options):

        users = User.objects.all()

        today = timezone.now().date()
        new_products = Product.objects.filter(created_at__date=today)

        if new_products.exists():
            subject = 'New Products Added Today'
            message = 'The following new products have been added today:\n\n'
            for product in new_products:
                message += f'{product.name}: {product.description}\n'
            message += '\n\nVisit our website to see more details.'

            for user in users:
                send_mail(subject, message, 'aralovjavoxir@gmail.com', [user.email])

            self.stdout.write(self.style.SUCCESS('Email notifications sent successfully'))
        else:
            self.stdout.write(self.style.WARNING('No new products added today'))
