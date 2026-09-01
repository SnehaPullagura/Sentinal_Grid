from __future__ import annotations
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
