import os
from dotenv import load_dotenv
import jwt
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import re
import bcrypt
from brevo import AsyncBrevo
import secrets
from Backend.database.database import users
from datetime import datetime, timedelta
class Signin(BaseModel):
    name: str
    email:str
    password:str


load_dotenv()
brevo_client = AsyncBrevo(api_key=os.getenv("BREVO_API_KEY"))

async def signin(data : Signin):

    try:

     exist = users.find_one({
        "email" : data.email
     })

     if exist and exist["isVerified"] == True:
        return JSONResponse(status_code=400 , content={"message" : "User already exist"})


     strongPassword = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
     hashedPassword = bcrypt.hashpw(data.password.encode() , bcrypt.gensalt())
  
     if not re.match(strongPassword, data.password):
        return  JSONResponse(status_code=400 , content={"message": "Strong password needed"})
     
         
     
     
     otp = str(secrets.randbelow(900000) + 100000)
     otpExpiry = datetime.now() + timedelta(minutes=10)


     if exist and exist["isVerified"] == False:
        update = users.find_one_and_update(
           {
           "email" : data.email
        } ,

        {"$set" : {
           "name": data.name,
                "email": data.email,
                "password":hashedPassword,
                "otp": otp,
                "otpExpiry": otpExpiry,
                
        }
        },
         return_document=True
        )


     else:
         create = users.insert_one({
                "name":data.name,
                "email":data.email,
                "password":data.password,
                "otp" : otp,
                "otpExpiry": otpExpiry,
                "isVerified": False
             })
        
  



     await brevo_client.send_email(
        sender= {"name" : "CrewAi" , "email": os.getenv("SENDER_EMAIL")},
        to=[{"email" : data.email}],
        subject="Verify your email",
        html_content= f"""Hi {data.name},
Use the verification code below to verify your email address and complete your CrewAI registration.

Your verification code: {otp}

This code expires in 10 minutes. If you didn't request this code, please ignore this email.

Regards,
The CrewAI Team
"""
     )


     return JSONResponse(status_code=200 , content={"message" : "Email successfully sent"})
      





    except Exception as error:
        return JSONResponse(status_code=200 , content={"message" : "internal server error"})
