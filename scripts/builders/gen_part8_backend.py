import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 8: FastAPI Backend & Services...")

    # 1. backend/app/core/config.py
    write_file("backend/app/core/config.py", """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel Grid Backend Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "sentinel_grid_production_super_secret_jwt_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = "sqlite:///./sentinel_grid.db"

    class Config:
        case_sensitive = True

settings = Settings()
""")

    # 2. backend/app/core/database.py
    write_file("backend/app/core/database.py", """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

    # 3. backend/app/auth/models.py
    write_file("backend/app/auth/models.py", """from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
""")

    # 4. backend/app/leaderboard/models.py
    write_file("backend/app/leaderboard/models.py", """from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.app.core.database import Base

class LeaderboardEntry(Base):
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(50), index=True, nullable=False)
    map_id = Column(String(50), index=True, nullable=False)
    score = Column(Integer, index=True, nullable=False)
    waves_cleared = Column(Integer, nullable=False)
    game_mode = Column(String(20), default="campaign")
    created_at = Column(DateTime, default=datetime.utcnow)
""")

    # 5. backend/app/replay/models.py
    write_file("backend/app/replay/models.py", """from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.app.core.database import Base

class ReplayRecord(Base):
    __tablename__ = "replays"

    id = Column(Integer, primary_key=True, index=True)
    replay_id = Column(String(64), unique=True, index=True, nullable=False)
    player_name = Column(String(50), nullable=False)
    map_id = Column(String(50), nullable=False)
    final_score = Column(Integer, nullable=False)
    replay_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
""")

    # 6. backend/app/main.py
    write_file("backend/app/main.py", """from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.core.database import engine, Base, get_db
from backend.app.auth.models import User
from backend.app.leaderboard.models import LeaderboardEntry
from backend.app.replay.models import ReplayRecord
from pydantic import BaseModel
from typing import List, Optional
import hashlib
import uuid

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    is_admin: bool

class LeaderboardSubmit(BaseModel):
    player_name: str
    map_id: str
    score: int
    waves_cleared: int
    game_mode: str = "campaign"

class ReplaySubmit(BaseModel):
    player_name: str
    map_id: str
    final_score: int
    replay_json: str

@app.get("/health")
def health():
    return {"status": "healthy", "service": "sentinel-grid-backend", "version": "1.0.0"}

@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    pwd_hash = hashlib.sha256(req.password.encode()).hexdigest()
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        # Auto-create for seamless zero-friction gameplay
        user = User(
            username=req.username,
            email=f"{req.username}@sentinelgrid.io",
            hashed_password=pwd_hash,
            is_admin=True if req.username.lower() in ("admin", "commander") else False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return TokenResponse(
        access_token=f"token_{user.username}_{uuid.uuid4()}",
        username=user.username,
        is_admin=user.is_admin
    )

@app.get("/api/v1/leaderboard", response_model=List[dict])
def get_leaderboard(map_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(LeaderboardEntry)
    if map_id:
        q = q.filter(LeaderboardEntry.map_id == map_id)
    entries = q.order_by(LeaderboardEntry.score.desc()).limit(50).all()
    if not entries:
        # Seed top scores
        return [
            {"rank": 1, "player_name": "Aegis_Prime", "map_id": "map_alpha_outpost", "score": 45800, "waves_cleared": 15},
            {"rank": 2, "player_name": "GridCommander", "map_id": "map_alpha_outpost", "score": 38200, "waves_cleared": 14},
            {"rank": 3, "player_name": "VortexTactician", "map_id": "map_alpha_outpost", "score": 31500, "waves_cleared": 12}
        ]
    return [
        {"rank": i + 1, "player_name": e.player_name, "map_id": e.map_id, "score": e.score, "waves_cleared": e.waves_cleared}
        for i, e in enumerate(entries)
    ]

@app.post("/api/v1/leaderboard/submit")
def submit_score(entry: LeaderboardSubmit, db: Session = Depends(get_db)):
    row = LeaderboardEntry(
        player_name=entry.player_name,
        map_id=entry.map_id,
        score=entry.score,
        waves_cleared=entry.waves_cleared,
        game_mode=entry.game_mode
    )
    db.add(row)
    db.commit()
    return {"status": "recorded", "score": entry.score}

@app.post("/api/v1/replays/submit")
def submit_replay(req: ReplaySubmit, db: Session = Depends(get_db)):
    rep_id = f"rep_{uuid.uuid4().hex[:12]}"
    rec = ReplayRecord(
        replay_id=rep_id,
        player_name=req.player_name,
        map_id=req.map_id,
        final_score=req.final_score,
        replay_json=req.replay_json
    )
    db.add(rec)
    db.commit()
    return {"status": "saved", "replay_id": rep_id}

@app.get("/api/v1/replays/{replay_id}")
def get_replay(replay_id: str, db: Session = Depends(get_db)):
    rec = db.query(ReplayRecord).filter(ReplayRecord.replay_id == replay_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Replay not found")
    return {"replay_id": rec.replay_id, "player_name": rec.player_name, "replay_json": rec.replay_json}
""")

    print("Part 8 Backend Complete.")

if __name__ == "__main__":
    generate()
