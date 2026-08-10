from app.utils.security import hash_password, verify_password
import jwt
import pytest

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

def test_hash_password():
    password = "password123"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_correct_password():
    password = "password123"

    hashed_password = hash_password(password)

    result = verify_password(
        password,
        hashed_password,
    )

    assert result is True


def test_verify_wrong_password():
    password = "password123"

    hashed_password = hash_password(password)

    result = verify_password(
        "wrongpassword",
        hashed_password,
    )

    assert result is False


def test_create_access_token():
    token = create_access_token(123)

    assert isinstance(token, str)
    assert len(token) > 0

def test_decode_access_token():
    token = create_access_token(123)

    payload = decode_access_token(token)

    assert payload["sub"] == "123"


def test_decode_invalid_access_token():
    invalid_token = "not-a-valid-token"

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(invalid_token)