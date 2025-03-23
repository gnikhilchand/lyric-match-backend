from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pydantic import BaseModel
from openai import OpenAI  # Import the OpenAI client
import random
from dotenv import load_dotenv

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lyricmatch.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the UserScore model
class UserScore(Base):
    __tablename__ = "user_scores"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    score = Column(Integer, default=0)

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the OpenRouter.ai client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # OpenRouter.ai API base URL
    api_key="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"  # Replace with your OpenRouter.ai API key
)

# List of song titles
song_titles = [
    "womenizer", "careless whisper", "Shape of You", " flowers",
    "Blinding Lights", "believer", "harleys in hawaii", "play date", "Uptown Funk",
    "snow man", "heathens", "Bad Guy", "take on me", "billie jean", "rasputin",
    "chandelier", "cheap thrills", "gloria", "new rules", "Opps I did it again",
]

class LyricRequest(BaseModel):
    song_title: str

class GuessRequest(BaseModel):
    user_guess: str
    correct_title: str
    username: str

class LeaderboardEntry(BaseModel):
    username: str
    score: int

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Welcome to the Lyric Match API!"}

@app.post("/generate-lyric")
async def generate_lyric():
    # Select a random song title
    song_title = random.choice(song_titles)

    # Prompt OpenRouter.ai to generate a lyric snippet
    prompt = f"Generate 2-4 lines of lyrics from the song '{song_title}' without revealing the song title."
    #prompt = "Generate 2-4 lines of lyrics from the telugu language songs without revealing the song title."
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",  # Use the DeepSeek model via OpenRouter.ai
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        extra_headers={
            "HTTP-Referer": "https://your-site-url.com",  # Optional. Replace with your site URL.
            "X-Title": "Lyric Match",  # Optional. Replace with your site name.
        },
        stream=False
    )

    # Extract the generated lyric snippet
    lyric_snippet = completion.choices[0].message.content.strip()
    #return {"lyric_snippet": lyric_snippet}
    return {"lyric_snippet": lyric_snippet, "correct_title": song_title}

# @app.post("/check-answer")
# async def check_answer(guess: GuessRequest):
#     # Check if the user's guess matches the correct title
#     is_correct = guess.user_guess.lower() == guess.correct_title.lower()
#     return {"is_correct": is_correct, "correct_title": guess.correct_title}

# @app.post("/check-answer")
# async def check_answer(guess: GuessRequest):
#     # Check if the user's guess matches the correct title
#     is_correct = guess.user_guess.lower() == guess.correct_title.lower()
#     if is_correct:
#         # Update the user's score in the database
#         query = scores.insert().values(username=guess.username, score=1)
#         await database.execute(query)
#     return {"is_correct": is_correct, "correct_title": guess.correct_title}

@app.post("/check-answer")
async def check_answer(guess: GuessRequest):
    db = SessionLocal()
    is_correct = guess.user_guess.lower() == guess.correct_title.lower()

    if is_correct:
        # Update user score
        user = db.query(UserScore).filter(UserScore.username == guess.username).first()
        if user:
            user.score += 1
        else:
            user = UserScore(username=guess.username, score=1)
            db.add(user)
        db.commit()

    db.close()
    return {"is_correct": is_correct, "correct_title": guess.correct_title}

# @app.get("/leaderboard")
# async def get_leaderboard():
#     # Fetch the top 10 scores from the database
#     query = scores.select().order_by(scores.c.score.desc()).limit(10)
#     leaderboard = await database.fetch_all(query)
#     return leaderboard

@app.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard():
    db = SessionLocal()
    leaderboard = db.query(UserScore).order_by(UserScore.score.desc()).limit(10).all()
    db.close()
    return leaderboard


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)