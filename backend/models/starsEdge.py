from sqlalchemy import Column, Integer, PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint

from db.connection import Base

class StarsEdge(Base):
    __tablename__ = "starsedges"

    se_star_a = Column(Integer, nullable=False)
    se_star_b = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('se_star_a <> se_star_b', name='se_different_stars'),
        PrimaryKeyConstraint("se_star_a", "se_star_b", name="se_pk"),
        ForeignKeyConstraint(["se_star_a"], ["stars.star_hip"], name="se_star_a_fk", ondelete="CASCADE", onupdate="CASCADE"),
        ForeignKeyConstraint(["se_star_b"], ["stars.star_hip"], name="se_star_b_fk", ondelete="CASCADE", onupdate="CASCADE"),
    )