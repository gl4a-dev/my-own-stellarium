from fastapi import FastAPI

from routes.constellation_routes import constellation_router

app = FastAPI()
app.include_router(constellation_router)