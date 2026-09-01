from __future__ import annotations
import uuid
from typing import Optional, Dict
from sqlalchemy.orm import Session
from backend.app.replay.models import ReplayRecord

class ReplayService:
    @staticmethod
    def save_replay(db: Session, player_name: str, map_id: str, final_score: int, replay_json: str) -> ReplayRecord:
        rep_id = f"rep_{uuid.uuid4().hex[:12]}"
        record = ReplayRecord(
            replay_id=rep_id,
            player_name=player_name,
            map_id=map_id,
            final_score=final_score,
            replay_json=replay_json
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_replay_by_id(db: Session, replay_id: str) -> Optional[ReplayRecord]:
        return db.query(ReplayRecord).filter(ReplayRecord.replay_id == replay_id).first()
