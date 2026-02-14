from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the base class for all models
Base = declarative_base()

# Database file 
DATABASE_URL = "sqlite:///use_cases.db"

# Create engine (connection to database)
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory (for database operations)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Function to get database session.
    
    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()