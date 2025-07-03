from fastapi import Request , Depends , HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
import jwt
import os
import dotenv

dotenv.load_dotenv()
JWT_TOKEN = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'

security = HTTPBearer()

def verify_token(credentials : HTTPAuthorizationCredentials = Depends(security)):
   try:
    paylod = jwt.decode(credentials.credentials ,JWT_TOKEN , JWT_ALGORITHM )
    return paylod
   
   except jwt.ExpiredSignatureError:
     raise HTTPException(status_code=401 , detail="Token expired")
   
   except jwt.InvalidTokenError:
     raise HTTPException(status_code=401 , detail="Invalid Token")
    