import enum

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
    SEAT_NOT_ALLOWED_FOR_MEDICAL = 15,
    CHARGEABLE = 16,
    LAVATORY = 17,
    BLOCKED_SEAT_PERMANENT = 18

class Availability:
    value: bool = False
    conditions = []
    
    def __init__(self, value:bool, conditions:list):
        self.value = value
        self.conditions = conditions
    
    def jsonRepr(self):
        return {
            "value": self.value,
            "conditions": self.conditions,
        }