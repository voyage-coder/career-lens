from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
class RegisterIn(BaseModel): name:str; email:EmailStr; password:str
class LoginIn(BaseModel): email:EmailStr; password:str
class UserOut(BaseModel):
    id:int; name:str; email:EmailStr
    model_config=ConfigDict(from_attributes=True)
class TokenOut(BaseModel): access_token:str; token_type:str="bearer"; user:UserOut
class ResumeOut(BaseModel):
    id:int; filename:str; created_at:datetime
    model_config=ConfigDict(from_attributes=True)
class JobMatchIn(BaseModel): resume_id:int; job_description:str
