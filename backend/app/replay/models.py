from sqlalchemy import Column, Integer, String, Text, DateTime
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
