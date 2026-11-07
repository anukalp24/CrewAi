
 
from Backend.database.database import users
import re
import os
import jwt
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import bcrypt
from datetime import datetime , timedelta
class Login(BaseModel):
 email:str
 password: str


async def login (data: Login):


 try:
 
  exist = users.find_one({
  "email" : data.email
 })

  if  not exist:
   return JSONResponse(status_code=404 , content={"message" : "User not found"})

  if not bcrypt.checkpw(data.password.encode() , exist["password"].encode()):
   return JSONResponse(status_code=400 , content={"message" : "Incorrect Password"})
 
  if exist["isVerified"] == False:
   return JSONResponse(status_code=400 , content={"message" : "user not verified"})
 

# token
  accessToken = jwt.encode(
{"id": str(exist["_id"]),
 "exp" : datetime.utcnow() + timedelta(minutes=15)
 } ,
 os.getenv("JWT_ACCESS_TOKEN"),
 algorithm="HS256"
)

  refreshToken = jwt.encode(
{"id" : str(exist["_id"]) ,
"exp" : datetime.utcnow() + timedelta(days=30)
 },
 os.getenv("JWT_REFRESH_TOKEN"),
 algorithm="HS256"
)



 
  update = users.update_one(

   {"email" : data.email} ,

   {"$set" : {
     "refreshToken" : refreshToken
   }}
 )

  response = JSONResponse(status_code=200 , content={"message" : "logged in successfully"})

  response.set_cookie(
 key="accessToken",
   value=accessToken,
 httponly=True,
     secure=True,
     samesite="none",
     max_age=15* 60
)


  response.set_cookie(
 key="refreshToken",
 value=refreshToken,
    httponly=True,
     secure=True,
     samesite="none",
     max_age=30 * 24 * 60 * 60
)
  return response

 except Exception as error:
  print(error)
  return JSONResponse(status_code=500 , content={"message" : "Internal server error"})
