import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import get_config


def create_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    return private_key, public_key


def save_keys(
        private_key: rsa.RSAPrivateKey,
        public_key: rsa.RSAPublicKey,
        password: str
) -> None:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt="".encode(),
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    private_key_encrypted = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(key)
    )

    config = get_config()

    if not os.path.exists(config.KEY_PATH):
        os.mkdir(config.KEY_PATH)

    private_key_path = os.path.join(config.KEY_PATH, 'private_key.pem')
    public_key_path = os.path.join(config.KEY_PATH, 'public_key.pem')

    with open(private_key_path, "wb") as private_key_file:
        private_key_file.write(private_key_encrypted)

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_key_path, "wb") as public_key_file:
        public_key_file.write(public_key_pem)


def is_keys_exist() -> bool:
    config = get_config()
    return (
            os.path.exists(config.KEY_PATH) and
            os.path.exists(os.path.join(config.KEY_PATH, "private_key.pem")) and
            os.path.exists(os.path.join(config.KEY_PATH, "public_key.pem"))
    )


def try_load_keys(
        password: str
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey] | None:
    config = get_config()
    if not os.path.exists(config.KEY_PATH):
        create_keys()

    if not is_keys_exist():
        return None

    private_key_path = os.path.join(config.KEY_PATH, 'private_key.pem')
    public_key_path = os.path.join(config.KEY_PATH, 'public_key.pem')

    with open(private_key_path, 'rb') as private_key_file:
        encrypted_private_key = private_key_file.read()

    # Derive a key from the password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt="".encode(),
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Decrypt the private key
    private_key = serialization.load_pem_private_key(
        encrypted_private_key,
        password=key,
        backend=default_backend()
    )

    # Load the public key from file
    with open(public_key_path, 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )

    return private_key, public_key


def public_key_to_string(public_key):
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    public_key_str = public_key_pem.decode('utf-8')

    return public_key_str
