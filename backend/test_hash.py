from backend.auth.security import (
    hash_password,
    verify_password
)

password = "hello123"

hashed = hash_password(password)

print("Original:", password)
print("Hashed:", hashed)

print(
    verify_password(
        "hello123",
        hashed
    )
)

print(
    verify_password(
        "wrongpass",
        hashed
    )
)