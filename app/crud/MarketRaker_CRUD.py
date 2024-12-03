from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import base64
import json
from decouple import config


SIGNING_KEY = str(config("SIGNING_KEY"))
APPLICATION_ID = str(config("APPLICATION_ID"))
public_key_str = str(config("public_key_str"))
public_key_str = public_key_str.replace("\\n","\n")

############################## Validate the indicator that was send from the marketraker api
def verify_signature(payload: json, signature: str, public_key_str: str) -> bool:
    """
    Verifies the signature of a payload.

    Parameters:
    - payload (json): The payload that was signed.
    - signature (str): The base64 encoded signature to verify.
    - public_key_str (str): The PEM formatted public key string.

    Returns:
    - bool: True if the signature is valid, False otherwise.
    """
    try:
        payload_bytes: bytes = payload.encode("utf-8")
        signature_bytes: bytes = base64.b64decode(signature.encode("utf-8"))

        public_key = serialization.load_pem_public_key(
            public_key_str.encode("utf-8"), backend=default_backend()
        )

        public_key.verify(
            signature_bytes,
            payload_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"An error occurred during signature verification: {e}")
        return False


def decision_maker(Acceptable_Risk: int, Indicator_Risk: int) -> bool:
    return True if Acceptable_Risk >= Indicator_Risk else False


