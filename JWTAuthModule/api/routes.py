from fastapi import HTTPException, Depends, APIRouter
from database import database
from models import users
from schema import User, UserRegister, UserLogin, Token, TokenRefreshRequest
from passlib.context import CryptContext
from auth.jwt_handler import create_access_token, refresh_token, decode_token
from auth.jwt_bearer import JWTBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=['users']
)

def hash_password(password: str):
    return pwd_context.hash(password)

# CREATE A USER
@router.post('/register/', response_model=User)
async def register_user(user: UserRegister):
    try:
        query = users.insert().values(name=user.name, email=user.email, password=hash_password(user.password), role=user.role)
        user_id = await database.execute(query)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    
    return {**user.dict(), "id": user_id}

# GET USER BY ID
@router.get('/users/{user_id}', response_model=User)
async def get_user_by_id(user_id: int):
    
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# LOGIN USER
@router.post("/login/", response_model=Token)
async def login_user(user: UserLogin):
    query = users.select().where(users.c.email == user.email)
    db_user = await database.fetch_one(query)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    data = {"sub": user.email, "role": db_user["role"]}
    
    return {
        "access_token": create_access_token(data),
        "refresh_token": refresh_token(data),
        "token_type":"bearer"
        }

# ADMIN LOGIN WITH ROLE AND JWT TOKEN
@router.get('/admin-only', dependencies=[Depends(JWTBearer(roles=['Admin']))])
def admin_dashboard():
    return {"message": "Welcome Admin"}

# GET ACCESS TOKEN FROM REFRESH TOKEN
@router.post('/refresh/')
def refresh_user_token(payload: TokenRefreshRequest):
    decode = decode_token(payload.token)
    if not decode or decode.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    data = {
        "sub": decode['sub'],
        "role": decode['role']
    }
    
    access_token = create_access_token(data)
    return {"access_token": access_token}