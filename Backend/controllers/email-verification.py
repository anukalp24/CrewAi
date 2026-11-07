import os
from fastapi.responses import JSONResponse
from pydantic import BaseModel , EmailStr
from Backend.database.database import users
import jwt
from datetime import datetime , timedelta
import re


class verification(BaseModel):
 email: EmailStr

# fastapi here passes the instance to the function

async def emailVerification(request : verification):
 try:
 
  exist =  users.find_one({
   "email" : request.email
 })

  if not exist:
    return JSONResponse(status_code=404  , content={"message" : "no user found"})

  if exist["isVerified"] == True:
   return JSONResponse(status_code=400 , content={"message" : "User already verified"})

   
 
  if exist["otp"] != request.otp:
   return JSONResponse(status_code=400 , content={"message" : "Invalid otp"})

  if datetime.now() > exist["otpExpiry"] :
    return JSONResponse(status_code=400 , content={"message" : "The otp is expired "})


  accessToken = jwt.encode(

   {
    "id" : str(exist["_id"]) ,
    "exp" : datetime.utcnow() + timedelta(minutes=15)
   } ,

   os.getenv("JWT_SECRET"),
   algorithm="HS256"


  )



  refreshToken = jwt.encode(
      {
       "id" : str(exist["_id"]) , 
       "exp": datetime.utcnow() + timedelta(days=30)
       } ,
       os.getenv("JWT_REFRESH_SECRET"),
      algorithm="HS256"
  )


  response =  JSONResponse(status_code=200 , content={"message" : "user verified successfully"})
  response.set_cookie()   
  response.set_cookie(key="refreshToken"
                       , value=refreshToken,
                       httponly=True,
    secure=True,
    samesite="none",
    max_age=30 * 24 * 60 * 60

                       )

  
  response.set_cookie(key="accessToken"
                       , value=accessToken,
httponly=True,
    secure=True,
    samesite="none",
    max_age=15* 60


                       )
  return response




 except Exception as error:
  return JSONResponse(status_code=500  , content={"message" : "Internal server error"})