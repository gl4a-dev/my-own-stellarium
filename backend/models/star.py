from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint, ForeignKeyConstraint

from db.connection import Base

class Star(Base):
    __tablename__ = "stars"

    star_hip = Column(Integer, nullable=False)
    star_name = Column(String(100), nullable=False)
    star_ra = Column(Float, nullable=False)
    star_dec = Column(Float, nullable=False)
    star_vmag = Column(Float, nullable=False) 
    star_bv_index = Column(Float, nullable=True) 
    star_constellation = Column(String(3), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("star_hip", name="star_pk"),
        ForeignKeyConstraint(["star_constellation"], ["constellations.constellation_iau"], name="star_constellation_fk", ondelete="CASCADE", onupdate="CASCADE")
    )

