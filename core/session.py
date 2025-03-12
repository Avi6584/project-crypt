from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'mysql+pymysql://root:Admin123@localhost:3306/crypto'

engine = create_engine(URL_DATABASE, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


