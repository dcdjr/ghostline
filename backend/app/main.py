from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from uuid import uuid4

from datetime import datetime, timezone

from app.db import init_db, insert_room


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/api/rooms")
def rooms() -> dict[str, str]:
    room_id = str(uuid4())
    created_at = _get_iso()

    insert_room(room_id, created_at)

    return {
        "id": room_id,
        "created_at": created_at,
    }
