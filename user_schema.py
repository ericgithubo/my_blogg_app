from pydantic import BaseModel

class postBase(BaseModel):
   tittle:str
   content:str
   published:bool = True

class postCreate(postBase):
   pass

class post(BaseModel):
   
   tittle:str
   content:str
   published:bool

class userCreate(BaseModel):

   first_name:str
   last_name:str
   email:str
   password:str

class Login(BaseModel):
   email:str
   password:str