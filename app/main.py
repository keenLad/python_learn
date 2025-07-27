from fastapi import FastAPI
from app.views import api, html
from app.database import engine
from app.models.person import Base

app = FastAPI(title="People API")
Base.metadata.create_all(bind=engine)
app.include_router(api.router)
app.include_router(html.router)
