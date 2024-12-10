#provient du tutoriel : https://www.youtube.com/watch?v=wB1qOExDsYY
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationtokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

account_activation_token = AccountActivationtokenGenerator()