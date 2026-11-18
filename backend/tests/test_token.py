
from jose import jwt
from datetime import datetime, timezone

from app.security import create_token
from app.core.config import settings


def test_create_token():
    token = create_token(1)

    assert isinstance(token, str)
    assert len(token) > 0


def test_token_contains_correct_user_id():
    token = create_token(123)

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"]
    )

    assert payload["sub"] == "123"


def test_token_expiration_is_future():
    token = create_token(1)

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"]
    )

    expiry = datetime.fromtimestamp(
        payload["exp"], timezone.utc
    )

    assert expiry > datetime.now(timezone.utc)
