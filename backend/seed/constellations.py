import json
from pathlib import Path

from db.session import SessionLocal
from models.constellation import Constellation

def load_constellations() -> list[dict]:
    DATA_PATH = Path(__file__).parent / "datasets" / "iau_constellations.json"
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def insert_constellations(constellations:list[dict]):
    with SessionLocal() as session:
        for item in constellations:
            obj = Constellation(**item)
            session.add(obj)

        session.commit()
    
if __name__ == "__main__":
    constellations = load_constellations()
    insert_constellations(constellations)