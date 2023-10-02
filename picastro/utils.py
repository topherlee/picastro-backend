from django.core.mail import EmailMessage


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
