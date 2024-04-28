# utils.py
from django.contrib.auth.hashers import check_password
from django.conf import settings

def get_decrypted_name(encrypted_name):
    # Iterate through a list of possible password hashers
    for hasher in settings.PASSWORD_HASHERS:
        try:
            # Attempt to decrypt the encrypted name using the current hasher
            decrypted_name = hasher.decrypt(encrypted_name)
            # If successful, return the decrypted name
            return decrypted_name
        except Exception:
            # If decryption fails with the current hasher, try the next one
            continue
    # If no hasher could decrypt the name, return None
    return None