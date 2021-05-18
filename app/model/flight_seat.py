from app.model.price import Price
import enum

class SeatLocation(enum.Enum):
    WINDOW = 1
    CENTER = 2
    AISLE = 3

class SeatCondition(enum.Enum):
    WING = 1,
    EXIT = 2,
    SEAT_SUITABLE_FOR_ADULT_WITH_AN_INFANT = 3,
    SEAT_IN_A_QUIET_ZONE = 4,
    SEAT_NOT_SUITABLE_FOR_CHILD = 5,
    SEAT_NOT_ALLOWED_FOR_INFANT = 6,
    RESTRICTED_RECLINE_SEAT = 7,
    SEAT_TO_BE_LEFT_VACANT_OR_OFFERED_LAST = 8,
    LEG_SPACE_SEAT = 9,
    SEAT_WITH_FACILITIES_FOR_HANDICAPPED = 10,
    SEAT_WITH_FACILITIES_FOR_HANDICAPPED_INCAPACITATED_PASSENGER = 11,
    SEAT_SUITABLE_FOR_UNACCOMPANIED_MINORS = 12,
    REAR_FACING_SEAT = 13,
    CREW_SEAT = 14,
    SEAT_NOT_ALLOWED_FOR_MEDICAL = 15

class Availability:
    value: bool = False
    conditions = []
    def __init__(self, value:bool, conditions:list):
        self.value = value
        self.conditions = conditions

class CabinType(enum.Enum):
    ECONOMY = 1
    FIRST = 2

class FlightSeat:
    rowNumber = ""
    location = ""
    cabinClass = ""
    seatId = ""
    availability = Availability(value=False, conditions=[])
    price = Price(totalAmount=0.0, currency=""),


    def __init__(self, location: str, cabinClass: str, seatId: str, 
    availability: Availability, price: Price, rowNumber: str):
        self.location = location
        self.cabinClass = cabinClass
        self.seatId = seatId
        self.availability = availability
        self.price = price
        self.rowNumber = rowNumber