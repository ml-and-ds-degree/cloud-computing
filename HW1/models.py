from typing import NamedTuple

from pydantic import BaseModel


class EntryData(NamedTuple):
    ticket_id: str
    plate: str
    parkingLot: str
    entry_time: str


class Receipt(BaseModel):
    plate: str
    total_parked_time: str
    parking_lot_id: str
    charge: str
