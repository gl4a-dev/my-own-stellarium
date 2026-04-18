from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint

from db.connection import Base

class Constallation(Base):
    __tablename__ = "constellations"

    constellation_iau = Column(String(3), nullable=False)
    constallation_la_name = Column(String(30), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('constellation_iau', name='constellation_pk'),
    )

