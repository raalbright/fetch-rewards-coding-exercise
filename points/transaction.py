from sqlalchemy import Column, Integer, String, DateTime
from .db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    payer = Column(String)
    points = Column(Integer)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f"Transaction<id={self.id!r}, payer={self.payer!r}, points={self.points!r}) timestamp={self.timestamp!r}>"