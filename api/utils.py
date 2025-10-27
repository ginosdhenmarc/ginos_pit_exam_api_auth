from django.core import signing
from django.conf import settings
from datetime import timedelta

SIGNING_SALT = 'email-verification-salt'
TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24  # 24 hours

def make_verification_token(user):
    data = {'user_id': user.pk}
    token = signing.dumps(data, salt=SIGNING_SALT)
    return token

def verify_verification_token(token):
    try:
        data = signing.loads(token, salt=SIGNING_SALT, max_age=TOKEN_MAX_AGE_SECONDS)
        return data
    except signing.BadSignature:
        return None
    except signing.SignatureExpired:
        return None
