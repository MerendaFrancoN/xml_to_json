# XML To JSON - Seatmaps

## Problem assumptions

 * seatmap1.xml 
    - Get the seat availability value from "availableInd" in <ns:Summary>
    - Unify "Fee" and "Taxes" into "totalAmount" output seat field
    - Use "extension" and Text from <ns:Feature> tags to get SeatConditions
 
 
 * seatmap2.xml 
    - Get the seat availability value if seat has any of the restrictions ("SD10", "SD11" and "SD19" ) and has "SD4" available seat definition
    - Set cabinType to PREFERENTIAL or ECONOMY according if seat has "SD16" definition

## JSON Output Format
  For the standardized JSON Format, I added beside the seats by row, the flight information.
  Some of the fields works with an enum behind, in an attempt to unify both formats into one.
  In the JSON output will have two fields, 
  - "flightData" which is a quick info of the flight where the seats are from
  - "seatsData" which has the seats objects by row


  ### Seat Fields
   - "rowNumber" - String indicating rowNumber of the seat
   - "location" - String indicating WINDOW,CENTER,AISLE, or NO_INFO seat location. Check **SeatLocation Enum**
   - "cabinClass" - String indicating class of the cabin, can be ECONOMY, FIRST or PREFERENTIAL. Check **CabinType Enum**
   - "cabinLayout" - String indicating the layout of the seats, e.g. "ABC DEF", useful for display seats info on front
   - "seatId" - String of the number of the seat, e.g. "7B"
   - "price" - **Price** object with "totalAmount" and "currency" fields in it.
   - "availability" -  **Availability** object with "value" which can be true or false, and "conditions" which specify the conditions of the seat. Check **SeatCondition Enum**
  
  An example of the seat object:
  
  
    $ {
        "rowNumber": "7",
        "location": "WINDOW",
        "seatId": "7A",
        "cabinClass": "ECONOMY",
        "cabinLayout": "ABC DEF",
        "price": {
          "totalAmount": 22.1,
          "currency": "GBP"
        },
        "availability": {
          "value": true,
          "conditions": [
            "SEAT_SUITABLE_FOR_ADULT_WITH_AN_INFANT",
            "SEAT_IN_A_QUIET_ZONE"
          ]
        }
      },
   
### FlightData Fields
   - "departureAirportCode" - String indicating departure airport code
   - "arrivalAirportCode" - String indicating airport code
   - "airEquipCode" - String indicating aircraft code
   - "flightNumber" - String indicating flight number
   - "departureDateTime" - String indicating datetime of departure in YYYY-MM-DDTHH:MM:SS format
  
  An example of the seat object:
  
  
    $ "flightData": {
    "departureAirportCode": "FNC",
    "arrivalAirportCode": "DUS",
    "airEquipCode": "320",
    "flightNumber": "1415",
    "departureDateTime": "2021-08-26T17:45:00"
  },

### Enums

#### SeatLocationEnum
    class SeatLocation(enum.Enum):
    WINDOW = 1
    CENTER = 2
    AISLE = 3
    NO_INFO = 4
    
#### SeatLocationEnum
    class CabinType(enum.Enum):
    ECONOMY = 1
    FIRST = 2
    PREFERENTIAL = 3

#### SeatConditionEnum
    $ class SeatCondition(enum.Enum):
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

