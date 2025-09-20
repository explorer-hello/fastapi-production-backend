from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# def get_conn():
#      return psycopg2.connect(
#          dbname="fastapi",
#          user="postgres",
#          password="sunny1312",
#          host="localhost",
#          port="5432"
#      )

# engine = create_engine("postgresql+psycopg2://",creator=get_conn,echo=True)



SQLALCHEMY_DATABASE_URL ='postgresql://postgres:sunny1312@localhost:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db= sessionlocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn= psycopg2.connect(host='localhost',database='fastapi',user ='postgres', password='sunny@13', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("databse connectioon sucessful")
#         break
#     except Exception as error:
#         print("connection failed")
#         print("error is",error)
#         time.sleep(2)
