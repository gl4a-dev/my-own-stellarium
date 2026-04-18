from sqlalchemy import Column, String, PrimaryKeyConstraint

from db.connection import Base

class Constellation(Base):
    __tablename__ = "constellations"

    constellation_iau = Column(String(3), nullable=False)
    constellation_la_name = Column(String(30), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('constellation_iau', name='constellation_pk'),
    )

