import time
from typing import List, Dict

from fastapi import WebSocket
from src.operations.router import start

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.start_times: Dict[WebSocket, float] = {}
        self.word_counts: Dict[WebSocket, int] = {}
        self.current_text = start()  # Инициализируем текущий текст при создании экземпляра

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)
        self.start_times[ws] = time.time()
        self.word_counts[ws] = 0

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)
        del self.start_times[ws]
        del self.word_counts[ws]

    async def calc_wpm(self, ws: WebSocket, text: str):
        current_time = time.time()
        elapsed_time = current_time - self.start_times[ws]
        word_count = len(text.strip())
        self.word_counts[ws] = word_count
        wpm = (word_count / elapsed_time) * 60
        return wpm

    async def checkText(self, text: str):
        is_correct = self.current_text.startswith(text)  # Используем текущий текст
        return is_correct

    async def isEnd(self, text: str):
        isEnd = len(self.current_text.strip()) == len(text.strip())
        return isEnd
