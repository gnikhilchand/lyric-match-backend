from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from databases import Database

# SQLite database URL
DATABASE_URL = "sqlite:///./lyricmatch.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the scores table
scores = Table(
    "scores",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, index=True),
    Column("score", Integer),
)

# Create the database and tables
metadata.create_all(bind=engine)

# Initialize the database connection
database = Database(DATABASE_URL)