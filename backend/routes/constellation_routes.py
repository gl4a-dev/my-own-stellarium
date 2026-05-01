from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text, TextClause
from sqlalchemy.orm import Session

from db.session import get_session
from models.constellation import Constellation
from models.star import Star

constellation_router = APIRouter(prefix="/constellations", tags=["constellations"])

@constellation_router.get("/all")
async def get_all_constellations(session:Session = Depends(get_session)):
    result = session.query(Constellation).all()
    return result

@constellation_router.get("/brighter-stars")
async def get_brighter_stars(iau:str, vmag:float = 5, session:Session = Depends(get_session)):
    query = text("""
        SELECT * 
        FROM stars 
        WHERE star_constellation = :iau AND star_vmag < :vmag
        ORDER BY star_vmag
    """)

    result = session.execute(query, {
        "iau": iau.upper(),
        "vmag": vmag
    })

    return result.mappings().all()
