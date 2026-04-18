from sqlalchemy.orm import sessionmaker

from db.connection import db_engine

SessionLocal = sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False
)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

if __name__ == "__main__":
    print(SessionLocal)