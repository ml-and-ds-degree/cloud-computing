from http import HTTPStatus

VEHICLE_ALREADY_PARKED = {HTTPStatus.BAD_REQUEST: {"description": "Vehicle already parked"}}

TICKET_NOT_FOUND = {HTTPStatus.NOT_FOUND: {"description": "Ticket not found"}}
