from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from app2 import sign, decode
import uvicorn

app = FastAPI()

userlist =[]

class SignUpSchema(BaseModel):
    name: str = "someoneidk"
    email: str = "someonenothing@gmail.com"
    password: str = "somethingidk"

@app.get("/")
def home():
    return "It's working. "
    # healthy

@app.post("/signup")
def sign_up(request: SignUpSchema):
    for user in userlist:
        if user.email == request.email:
            raise HTTPException(status_code=400, detail="Error. Email already registered")
        
    userlist.append(request)

    token = sign(request.email)

    for user in userlist:
        print(user.name, user.email, user.password)

    return token

class SignInSchema(BaseModel):
    email: str = "someoneemail@some.com"
    password: str = "somethingidk"


@app.post("/signin")
def sign_in(request: SignInSchema):
    for user in userlist:
        if user.email == request.email:
            if user.password == request.password:
                token = sign(user.email)
                return token
        else: 
            raise HTTPException(status_code=400, detail="Incorrect password!")
        
    raise HTTPException(status_code=400, detail="Incorrect email or email not registered!")



@app.post("/authtest")
def authtest(decode: str = Depends(decode)):
    return decode



if __name__ == "__main__":
    uvicorn.run(app, port=8000)






