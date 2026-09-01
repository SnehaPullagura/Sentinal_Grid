import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_deep_backend():
    print("--> Generating Comprehensive Backend Services...")

    # 1. backend/app/auth/service.py
    write_file("backend/app/auth/service.py", """from __future__ import annotations
import hashlib
import uuid
from typing import Optional, Dict
from sqlalchemy.orm import Session
from backend.app.auth.models import User

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return AuthService.hash_password(plain) == hashed

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.username == username).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def register_user(db: Session, username: str, email: str, password: str, is_admin: bool = False) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=AuthService.hash_password(password),
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
""")

    # 2. backend/app/leaderboard/service.py
    write_file("backend/app/leaderboard/service.py", """from __future__ import annotations
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.app.leaderboard.models import LeaderboardEntry

class LeaderboardService:
    @staticmethod
    def record_score(db: Session, player_name: str, map_id: str, score: int, waves_cleared: int, game_mode: str = "campaign") -> LeaderboardEntry:
        entry = LeaderboardEntry(
            player_name=player_name,
            map_id=map_id,
            score=score,
            waves_cleared=waves_cleared,
            game_mode=game_mode
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_top_scores(db: Session, map_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        q = db.query(LeaderboardEntry)
        if map_id:
            q = q.filter(LeaderboardEntry.map_id == map_id)
        results = q.order_by(LeaderboardEntry.score.desc()).limit(limit).all()
        return [
            {
                "rank": idx + 1,
                "player_name": r.player_name,
                "map_id": r.map_id,
                "score": r.score,
                "waves_cleared": r.waves_cleared,
                "created_at": r.created_at.isoformat() if r.created_at else ""
            }
            for idx, r in enumerate(results)
        ]
""")

    # 3. backend/app/replay/service.py
    write_file("backend/app/replay/service.py", """from __future__ import annotations
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
""")

if __name__ == "__main__":
    generate_deep_backend()
