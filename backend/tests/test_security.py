
from app.security import hash_password, verify_password


def test_password_hashing():
    password = "TestPassword123"

    hashed = hash_password(password)

    assert hashed != password
    assert hashed != ""
    assert verify_password(password, hashed)


def test_same_password_generates_different_hashes():
    password = "TestPassword123"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_correct_password_verification():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_incorrect_password_verification():
    password = "TestPassword123"
    hashed = hash_password(password)

    assert verify_password("WrongPassword123", hashed) is False
