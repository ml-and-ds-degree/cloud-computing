import math
from hashlib import md5
from http import HTTPStatus

import arrow
from fastapi import FastAPI, HTTPException

from HW1.errors import TICKET_NOT_FOUND, VEHICLE_ALREADY_PARKED
from HW1.models import EntryData, Receipt

app = FastAPI(debug=True)


DATABASE: dict[str, EntryData] = {}


@app.post("/entry", responses=VEHICLE_ALREADY_PARKED)
async def entry(plate: str, parkingLot: str) -> str:
    ticket_id = md5((plate).encode()).hexdigest()[:8]

    if ticket_id in DATABASE:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Vehicle already parked {ticket_id=}")

    DATABASE[ticket_id] = EntryData(
        ticket_id=ticket_id,
        plate=plate,
        parkingLot=parkingLot,
        entry_time=arrow.now().isoformat(),
    )

    return ticket_id


@app.get("/exit", response_model=Receipt, responses=TICKET_NOT_FOUND)
async def exit(ticket_id: str) -> Receipt:
    if ticket_id not in DATABASE:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ticket not found")

    entry_data = DATABASE.pop(ticket_id)
    entry_time = arrow.get(entry_data.entry_time)
    exit_time = arrow.now()
    duration = exit_time - entry_time
    duration_in_minutes = duration.total_seconds() / 60

    if duration_in_minutes < 15:
        cost = 0
    else:
        increments = math.ceil(duration_in_minutes / 15)
        cost = increments * (10 / 4)

    return Receipt(
        plate=entry_data.plate,
        total_parked_time=str(duration),
        parking_lot_id=entry_data.parkingLot,
        charge=f"${cost:.2f}",
    )
