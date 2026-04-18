import requests

from db.session import SessionLocal
from models.star import Star

def star_request(hip_number:int):
    name = f"HIP {hip_number}"
    data = requests.get(f"http://localhost:8090/api/objects/info?format=json&name={name}").json()

    return Star(
        star_hip = int(data.get("name").replace("HIP ", "")),
        star_name = data.get("localized-name"),
        star_ra = data.get("ra"),
        star_dec = data.get("dec"),
        star_vmag = data.get("vmag"),
        star_bv_index = data.get("bV"),
        star_constellation = data.get("iauConstellation").upper()
    )

def populate_stars(start=1, end=120000, batch_size=500):
    with SessionLocal() as db:

        existing = {
            s.star_hip
            for s in db.query(Star.star_hip).all()
        }

        batch = []

        for hip in range(start, end + 1):
            if hip in existing:
                continue

            try:
                star = star_request(hip)
                if star.star_constellation is None:
                    continue
                batch.append(star)

            except Exception:
                continue

            if len(batch) >= batch_size:
                db.bulk_save_objects(batch)
                db.commit()
                print(f"Inserted batch of {len(batch)}")
                batch.clear()

        if batch:
            db.bulk_save_objects(batch)
            db.commit()
            print(f"Inserted final batch of {len(batch)}")

if __name__ == "__main__":
    populate_stars()
