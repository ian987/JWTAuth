from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class TokenRefreshRequest(BaseModel):
    token: str
    