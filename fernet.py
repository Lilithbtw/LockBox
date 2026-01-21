import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

mstr_password = b"CHANGE_THIS"

def generate_salt(file: str):
    try:
        # Try to open salt if it exists
        with open(file, "rb") as f:
            salt = f.read()
        return salt
    except OSError:
        # Generate a random salt
        salt = os.urandom(16)
        with open(file, "wb") as f:
            f.write(salt)
        return salt
    except:
        os.remove(file)

        salt = os.urandom(16)
        with open(file,"wb") as f:
            f.write(salt)
        return salt

def main():
    salt = generate_salt("salt.bin")

    # Derive a Fernet-compatible 32-byte key:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(mstr_password))

    # Create the cipher
    cipher = Fernet(key)

    # Create encrypted message
    message = b"Message to encrypt"
    token = cipher.encrypt(message)

    CIPHER = "cipher.bin"

    if os.path.exists(CIPHER):
        try:
            # Try to open cipher if it exists
            with open(CIPHER, "rb") as f:
                cipher_db = f.read()
        except Exception:
            prev_mssg = None
    else:
        prev_mssg = None

    # Try to Decrypt with mstr_password
    try:
        cipher2 = Fernet(key)
        prev_mssg = cipher2.decrypt(cipher_db)

        if prev_mssg != message:
            print("Message changed!! Updating chipher.bin")
            with open(cipher, "wb") as f:
                f.write(token)
            prev_mssg = message
        else:
            pass

        print("Decrypted:", prev_mssg.decode("utf-8"))

        print("Cipher.bin: ", cipher_db)
    except Exception:
        print("Can't decrypt password!!!")
        print("Master Password does not match with stored password")

if __name__ == "__main__":
    main()
