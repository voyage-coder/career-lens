from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import get_db
from app.models import User
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth=OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_token(uid):
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":str(uid),"exp":exp},settings.secret_key,algorithm="HS256")
def get_current_user(token:str=Depends(oauth),db:Session=Depends(get_db)):
    err=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
    try: uid=int(jwt.decode(token,settings.secret_key,algorithms=["HS256"]).get("sub",""))
    except (JWTError,ValueError,TypeError): raise err
    user=db.query(User).filter(User.id==uid).first()
    if not user: raise err
    return user
