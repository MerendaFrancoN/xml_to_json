from app.model.price import Price
from app.model.availability import Availability
import enum

class SeatLocation(enum.Enum):
    WINDOW = 1
    CENTER = 2
    AISLE = 3
    NO_INFO = 4

class CabinType(enum.Enum):
    ECONOMY = 1
    FIRST = 2
    PREFERENTIAL = 3
    

class FlightSeat:
    rowNumber = ""
    location = ""
    cabinClass = ""
    cabinLayout = ""
    seatId = ""
    availability = Availability(value=False, conditions=[])
    price = Price(totalAmount=0.0, currency=""),


    def __init__(self, location: str, cabinClass: str, seatId: str, 
    availability: Availability, price: Price, rowNumber: str, cabinLayout: str):
        self.location = location
        self.cabinClass = cabinClass
        self.seatId = seatId
        self.availability = availability
        self.price = price
        self.rowNumber = rowNumber
        self.cabinLayout = cabinLayout
    
    def jsonRepr(self):
        return {
            "rowNumber": self.rowNumber,
            "location": self.location,
            "seatId": self.seatId,
            "cabinClass":self.cabinClass,
            "cabinLayout": self.cabinLayout,
            "price": self.price.jsonRepr(),
            "availability": self.availability.jsonRepr()
        }