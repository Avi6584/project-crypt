from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate a new EC key pair
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Export keys
vapid_private_key = base64.urlsafe_b64encode(private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)).decode('utf-8')

vapid_public_key = base64.urlsafe_b64encode(public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)).decode('utf-8')

print("Public Key:", vapid_public_key)
print("Private Key:", vapid_private_key)
