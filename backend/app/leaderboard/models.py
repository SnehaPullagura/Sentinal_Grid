from sqlalchemy import Column, Integer, String, Float, DateTime
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
