import secrets
from pathlib import Path

env_file = Path(".env")

secret_key = secrets.token_urlsafe(64)

with env_file.open("a") as f:
    f.write(f"\nSECRET_KEY={secret_key}\n")

print("Secret key created")