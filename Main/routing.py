from fastapi import FastAPI , HTTPException ,Depends
from Models.UserRegistration import UserRegistration 
from Models.UserLogin import UserLogin
from Dependencies.token_verify import verify_token
import mysql.connector
import os
import dotenv
import bcrypt
import jwt
from datetime import datetime , timedelta , timezone

dotenv.load_dotenv()
JWT_KEY = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'

salt = bcrypt.gensalt()
 
app = FastAPI()
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
    )

@app.get('/')
def root_route():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"result": result}

@app.post('/signup')
def register_user(user: UserRegistration):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8') , salt)


        insert_query = "INSERT INTO users (email, phone, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user.email, user.phone,hashed_password ))
        conn.commit()

        
        
        payload = {
            "email" : user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }

        token = jwt.encode(payload , JWT_KEY , JWT_ALGORITHM)


        return{
            "message" : "User registered successfully",
            "token" : token
        }

    except mysql.connector.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Email or phone number already exists.")
    finally:
        cursor.close()
        conn.close()


@app.post('/login')
def login_user(login : UserLogin):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        query = "SELECT password FROM users WHERE email =%s"
        cursor.execute(query , (login.email,))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404 , detail="User not found")
        
        stored_hashed_password = result[0]

        if(bcrypt.checkpw(login.password.encode('utf-8') , stored_hashed_password)):
            payload = {
                'email' : login.email,
                'exp' : datetime.now(timezone.utc) + timedelta(hours=1)
            }

            token = jwt.encode(payload , JWT_KEY , JWT_ALGORITHM)

            return {"message :" : "Logged in successfully" , "token" : token}
        
        else:
            raise HTTPException(status_code=401 , detail="Incorrect Password")
        
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
    

    finally:
        cursor.close()
        connection.close()



@app.get("/protected")
def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "Access granted ✅", "user": payload["email"]}
