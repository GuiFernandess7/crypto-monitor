from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class History(Base):
    __tablename__ = "crypto_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    current_balance = Column(Integer, nullable=False, default=0)
    currency = Column(String(3), nullable=False)

    def __repr__(self):
        return f"<History(id={self.id}>"
