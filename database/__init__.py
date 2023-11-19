from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import conf
from sqlalchemy.orm import Session

# sqlite:///./test.sqlite
# mysql://username:password@localhost/dbname

engine = create_engine(conf.database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)