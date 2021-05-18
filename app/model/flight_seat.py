from app.model.price import Price
import enum

class SeatLocation(enum.Enum):
    WINDOW = 1
    CENTER = 2
    AISLE = 3

class Availability:
    value: bool = False
    conditions = []
    def __init__(self, value:bool, conditions:list):
        self.value = value
        self.conditions = conditions


class FlightSeat:
    rowNumber = ""
    location = ""
    cabinClass = ""
    seatId = ""
    availability = Availability(value=False, conditions=[])
    price = Price(totalAmount=0.0, currency=""),


    def __init__(self, location: str, cabinClass: str, seatId: str, availability: Availability, price: Price, rowNumber: str):
        self.location = location
        self.cabinClass = cabinClass
        self.seatId = seatId
        self.availability = availability
        self.price = price
        self.rowNumber = rowNumber