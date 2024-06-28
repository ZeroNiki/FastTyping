import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.pages.router import router as router_pages

app = FastAPI(
    title="Type Test"
)

BASEDIR = os.path.dirname(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASEDIR, "src/static/")), name="static")


app.include_router(router_pages)


@app.get("/")
async def should():
    return "You should go to /pages/s"
