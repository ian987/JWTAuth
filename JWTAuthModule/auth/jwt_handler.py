from jose import jwt, JWTError
from datetime import datetime, timedelta
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTE, REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(data: dict):
    to_encode_data = data.copy()
    exp = datetime.utcnow() + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE))
    to_encode_data.update({'exp': exp, 'type':"access"})
    return jwt.encode(to_encode_data, SECRET_KEY, algorithm=ALGORITHM)

def refresh_token(data: dict):
    exp = datetime.utcnow() + (timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS))
    data.update({'exp': exp, 'type':"refresh"})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token:str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return None



