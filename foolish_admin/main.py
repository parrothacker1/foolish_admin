from fastapi import FastAPI,Response,status,Cookie,Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from foolish_admin import db
from foolish_admin.config import config

from pydantic import BaseModel
from rsa_python import rsa

import jwt as JWT
import random
import string
import math

from pathlib import Path


#app = FastAPI()
app = FastAPI(docs_url=None,redoc_url=None)

BASE_DIR=Path(__file__).resolve().parent
app.mount("/static",StaticFiles(directory=str(Path(BASE_DIR,'static'))),name="static")
templates=Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))
 
def rsa_encode(challenge_txt:str) -> str:
    keys=db.rsa_keys(add=False)
    if keys is None:
        key_pair=rsa.generate_key_pair(16)
        db.rsa_keys(add=True,keys=[key_pair["modulus"],key_pair['public'],key_pair["phi"]])
    else:
        n=keys[0]
        e=keys[1]
        key_pair={'public':int(e),'modulus':int(n)}
    encoded_text=rsa.encrypt(challenge_txt,int(key_pair['public']),int(key_pair['modulus']))
    return encoded_text

@app.get("/")
async def home(response:Response,
               request:Request,
               jwt: str | None = Cookie(default=None),
               sessionID: str | None = Cookie(default=None,alias="session-id")):
    response=templates.TemplateResponse('index.html',{"request":request,"guest":jwt is None})
    if jwt is None or sessionID is None:
        new_jwt=JWT.encode({'role':'guest','isAdmin':False},config["jwt_secret"],algorithm="HS512")
        new_session=''.join(random.choices(string.ascii_letters,k=8))
        db.add_session(new_session if sessionID is None else sessionID)
        response.set_cookie(key="jwt",value=new_jwt)
        response.set_cookie(key="session-id",value=new_session)
    return response

class Password(BaseModel):
    password:str

@app.post("/api/check_password")
async def check_password(password:Password,response:Response,jwt:str|None=Cookie(default=None)):
    result={"content":"wrong password","status_code":status.HTTP_401_UNAUTHORIZED}
    challenge_txt=open("challenge.txt","r+").read()
    if jwt is not None:
        jwt_header=JWT.get_unverified_header(jwt)
        decoded_jwt=JWT.decode(jwt,key=config['jwt_secret'],verify=False,algorithms=["HS512"],option={'verify_signature':True})
        if db.verify_password(password.password) and decoded_jwt['isAdmin'] and decoded_jwt['role']=='admin':
            result["content"]=rsa_encode(challenge_txt)
            result["status_code"]=status.HTTP_200_OK
        elif not decoded_jwt['isAdmin'] or not decoded_jwt['role'] =='admin':
            result["content"]="You are not allowed to use this api without admin jwt"
    else:
        result["content"]="No jwt is provided"
    response=JSONResponse(**result)
    return response

@app.get("/login")
async def admin_login(response:Response,
                      request:Request,
                      jwt: str | None = Cookie(default=None),
                      sessionID:str | None = Cookie(default=None,alias='session-id')):
    if sessionID is not None and jwt is not None:
        try:
            jwt_header=JWT.get_unverified_header(jwt)
            decoded_jwt=JWT.decode(jwt,
                               key=config["jwt_secret"],
                               verify=False,algorithms=['HS512'],
                               options={'verify_signature':True})
            response=templates.TemplateResponse('admin.html',{"request":request,"admin":decoded_jwt['isAdmin']})

            if decoded_jwt['isAdmin'] and decoded_jwt['role'] == "admin":
                db.session_checker(sessionID)
            else:
                response=templates.TemplateResponse('admin.html',{"request":request,"admin":False})
        except JWT.exceptions.InvalidSignatureError or JWT.exceptions.InvalidAlgorithmError:
            response=Response("Signature is not verified or algorithm is not same")
    
    return response

@app.get("/about")
async def admin_details(request:Request):
    return templates.TemplateResponse('about.html',{"request":request})

