from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker
from config import conf

# sqlite:///./test.sqlite
# mysql://username:password@localhost/dbname

engine = create_engine(conf.database, poolclass=pool.QueuePool, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
