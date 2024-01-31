from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['user_email_address']]
        )
        email.send()

    def get_user(self, request, format=None):
        token_user_id = request.user.id
        print("token_user_id", token_user_id)
        
        return token_user_id

    def send_token_email(relative_link, token,username, user_email):
        absolute_Url = settings.DOMAIN + relative_link + '?token='+token

        email_body = 'Hi ' + username + \
            ',\nUse link below to verify your email address for Picastro: \n' + absolute_Url
        data = {
            'email_subject': 'Verify your email for Picastro',
            'email_body': email_body,
            'user_email_address': user_email
        }

        print("body", email_body)
        print("email data", data)

        send_mail(
            'Verify your email for Picastro',
            email_body,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )

