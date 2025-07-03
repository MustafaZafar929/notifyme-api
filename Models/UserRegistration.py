from pydantic import BaseModel , EmailStr
class UserRegistration(BaseModel):
    email : EmailStr
    phone : str
    password : str