import hashlib
from datetime import datetime

def generate_secret_key():
    # Get the current time as a string
    current_time = datetime.utcnow().isoformat()

    # Create a hash of the current time
    hash_object = hashlib.sha256(current_time.encode())
    secret_key = hash_object.hexdigest()

    return secret_key
