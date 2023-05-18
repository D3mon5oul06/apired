from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/alpr"
engine = create_engine(DATABASE_URL)pip install mysql-connector-python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
