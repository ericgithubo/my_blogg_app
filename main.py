from fastapi import FastAPI ,Response,status,HTTPException
from typing import Optional,Annotated
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
import psycopg2
import time
from datetime import datetime
#from routers import user_router,post_router

import asyncpg
from app.user_schema import post,userCreate
from app import user_schema,utils
from psycopg2.extras import RealDictCursor


#from app import user,post








app = FastAPI()


#app.include_router(user_router.router)
#app.include_router(post_router.router)



while True:
   try:
      conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
                            password='ojede123',cursor_factory= RealDictCursor)
      cursor = conn.cursor()
      print("connection to the database succesful")
      break

   except Exception as error:
    print("conecting to database faild")
    print("error:",error)
    time.sleep(2)



my_posts =[{"tittle":"soccar","content":"i love footbal","id":1},
           {"title":"music","conten":"music is my other ob","id":2}]




@app.get("/")
def home():
    return " Hello,Welcome to the Alt-School BloggAPI! Look around at the _links to browse the API. And have a crazy-cool day."


@app.get("/posts")
def get_blogg():
   cursor.execute("""SELECT*FROM posts""")
   posts = cursor.fetchall()
   return{"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=user_schema.post)
def create_blogg(post: post):
   cursor.execute("""INSERT INTO posts(tittle,content,published) VALUES(%s,%s,%s) RETURNING
                 *""",(post.tittle,post.content,post.published))
   new_post = cursor.fetchone()

   conn.commit()
   return{"data":new_post}

@app.get("/posts/{id}")
def get_blog(id:str):
    cursor.execute("""SELECT*from posts WHERE id = %s """,(str(id)))
    post = cursor.fetchone()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    return {"post_detail":post}

@app.delete("/posts{id}",status_code=status.HTTP_204_NO_CONTENT)
def delet_blog(id:int):
   cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))
   delet_post = cursor.fetchone()
   conn.commit()

   if delet_post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"post with id:{id} does not exist")
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts{id}")
def update_blog(id:int,post:post):
   cursor.execute("""UPDATE posts SET tittle = %s, content = %s,published = %s WHERE id = %s
                  RETURNING *""",(post.tittle,post.content,post.published ,(str(id))))
   updated_post = cursor.fetchone()
   conn.commit()

   if update_blog == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id:{id} does not exist")
   return{"data":updated_post}
   

@app.post("/users",status_code=status.HTTP_201_CREATED)

def create_user(post: userCreate):
   hashed_password = utils.hash(post.password)
   post.password = hashed_password

   cursor.execute("""INSERT INTO users(first_name,last_name,email,password) VALUES(%s,%s,%s,%s) RETURNING
               *""",(post.first_name,post.last_name,post.email,post.password))
   new_user = cursor.fetchone()

    
   conn.commit()
   
   return{"data":new_user}


@app.get("/users/{id}")
def get_user(id:str):
    cursor.execute("""SELECT*from users WHERE id = %s """,(str(id)))
    post = cursor.fetchone()

    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    return {"post_detail":post}

   

@app.post("/login")
def login(post:user_schema.Login):


 
    email = login.email
    password = login.password

    if email in conn and conn[email]["password"] == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Login failed")
    


    