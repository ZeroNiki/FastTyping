import os
import json

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from src.operations.router import start
from .utils import ConnectionManager

manager = ConnectionManager()


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


BASEDIR = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(BASEDIR, "templates"))




@router.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    await ws.send_json({"initial_text": manager.current_text})
    try:
        while True:
            data = await ws.receive_text()

            if data == "restart":
                manager.current_text = start()
                await ws.send_json({"initial_text": manager.current_text})
            else:
                wpm = await manager.calc_wpm(ws, data)
                is_correct = await manager.checkText(data)
                is_end = await manager.isEnd(data)
                print(start())
                print(data)

                result = {"wpm": wpm, "is_correct": is_correct, "isEnd": is_end}
                await ws.send_text(json.dumps(result))

    except WebSocketDisconnect:
        manager.disconnect(ws)
        

@router.get("/s", response_class=HTMLResponse)
async def ss(req: Request):
    text = start()
    return templates.TemplateResponse("index.html", {"request": req, "text": text})

