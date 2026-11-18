
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.security import get_current_user
from app.core.config import settings


def test_get_current_user_valid_token():
    user = MagicMock()
    user.id = 1

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = user

    token = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=10)},
        settings.secret_key,
        algorithm="HS256"
    )

    result = get_current_user(token, db)

    assert result.id == 1


def test_get_current_user_invalid_token():
    db = MagicMock()

    with pytest.raises(HTTPException) as exc:
        get_current_user("invalid.token", db)

    assert exc.value.status_code == 401


def test_get_current_user_invalid_user_id():
    db = MagicMock()

    token = jwt.encode(
        {"sub": "invalid", "exp": datetime.now(timezone.utc) + timedelta(minutes=10)},
        settings.secret_key,
        algorithm="HS256"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token, db)

    assert exc.value.status_code == 401


def test_get_current_user_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    token = jwt.encode(
        {"sub": "999", "exp": datetime.now(timezone.utc) + timedelta(minutes=10)},
        settings.secret_key,
        algorithm="HS256"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token, db)

    assert exc.value.status_code == 401
