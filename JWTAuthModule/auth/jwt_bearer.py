from fastapi import HTTPException,Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from constants import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError


class JWTBearer(HTTPBearer):
    def __init__(self, roles: list = None, auto_error:bool = False):
        super().__init__(auto_error = auto_error)
        self.roles = roles
        
    async def __call__(self, request:Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials: 
            try:
                payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=ALGORITHM)
                if self.roles and payload.get("role") not in self.roles:
                    raise HTTPException(status_code=403, detail="Not enough permission")
                return payload
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid token")
        raise HTTPException(status_code=403, detail="Authorization required")
                