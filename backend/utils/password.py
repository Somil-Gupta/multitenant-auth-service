# from passlib.context import CryptContext  # type: ignore
import bcrypt
import random
import string
import base64

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
    
# def get_password_hash(password):
#     return pwd_context.hash(password)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    # Convert bytes to Base64 string
    return base64.b64encode(hashed_password).decode('utf-8')

def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    # Decode the Base64 hashed password back to bytes
    hashed_password_bytes = base64.b64decode(hashed_password)
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_bytes)