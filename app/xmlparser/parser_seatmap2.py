import xml.etree.ElementTree as ET
from app.model.flight_info import FlightInfo
from app.model.flight_seat import FlightSeat, Availability, SeatCondition, SeatLocation, CabinType
from app.model.price import Price


class Seat2MapParser:

    __namespaces = {
        'ns': "http://www.iata.org/IATA/EDIST/2017.2",
        'ns2': "http://www.iata.org/IATA/EDIST/2017.2/CR129"
    }

    __fileTree = None
    __fileRoot = None
    __offerItems = {}
    # init method or constructor

    def __init__(self, file):
        self.__fileTree = ET.parse(file)
        self.__fileRoot = self.__fileTree.getroot()
        #Dict - str -> Price
        self.__offerItems = self.__parseAlaCarteOffer()


    def __parseAlaCarteOffer(self):
        offerItemsDict = {}
        cartOffer = self.__fileRoot.find("ns:ALaCarteOffer",self.__namespaces)
        for item in cartOffer:
            itemKey = item.get("OfferItemID")
            try:
                offerItemsDict[itemKey] = Price(
                    currency=item.find("ns:UnitPriceDetail",self.__namespaces).find("ns:TotalAmount",self.__namespaces).find("ns:SimpleCurrencyPrice",self.__namespaces).get("Code"),
                    totalAmount=float(item.find("ns:UnitPriceDetail",self.__namespaces).find("ns:TotalAmount",self.__namespaces).find("ns:SimpleCurrencyPrice",self.__namespaces).text)
                )
            except :
                offerItemsDict[itemKey] = Price(currency="", totalAmount=0.0)
        
        return offerItemsDict

    def getFlightSeats(self):
        flightSeatList = []
        seatMapList = self.__fileRoot.findall("ns:SeatMap",self.__namespaces)
        for seatMap in seatMapList:
            #Dict str -> SeatLocation.name
            cabinLayoutDict = self.__parseCabinLayout(seatMap.find("ns:Cabin",self.__namespaces))
            seatRows = seatMap.find("ns:Cabin",self.__namespaces).findall("ns:Row",self.__namespaces)
            for row in seatRows:
                rowNumber = row.find("ns:Number",self.__namespaces).text
                seats = row.findall("ns:Seat",self.__namespaces)
                for seat in seats:
                    colNumber = seat.find("ns:Column",self.__namespaces).text
                    availability = self.__parseAvailability(seat)
                    price = Price(currency="", totalAmount=0.0)
                    if(availability.value):
                        priceRef = seat.find("ns:OfferItemRefs",self.__namespaces).text
                        price = self.__offerItems[priceRef]

                    flightSeatList.append(
                        FlightSeat(
                            rowNumber = rowNumber,
                            seatId=str(rowNumber)+str(colNumber),
                            availability=availability,
                            cabinClass=self.__parseCabinClass(seat),
                            location=cabinLayoutDict[colNumber],
                            price=price
                        )
                    )
        
        return flightSeatList
    

    def __parseCabinClass(self, seat):
        preferentialSeatClass = "SD16"
        seatDefs = self.__getSeatDefinitionsOfSeat(seat)
        if(any(preferentialSeatClass in seatDef for seatDef in seatDefs)):
            return CabinType.PREFERENTIAL.name
        else:
            return CabinType.ECONOMY.name

    def __parseCabinLayout(self, cabin : ET.Element):
        columns = cabin.find("ns:CabinLayout",self.__namespaces).findall("ns:Columns",self.__namespaces)
        cabinLayout = {}
        for column in columns:
            location = SeatLocation.WINDOW

            if(column.text == "WINDOW"):
                location = SeatLocation.WINDOW
            if(column.text == "AISLE"):
                location = SeatLocation.AISLE
            if(column.text == ""):
                location = SeatLocation.CENTER
            
            cabinLayout[column.get("Position")] = location.name

        return cabinLayout

    def __getSeatDefinitionsOfSeat(self, seat:ET.Element):
        return list(map((lambda elem : elem.text),seat.findall("ns:SeatDefinitionRef", self.__namespaces)))

    def __parseAvailability(self, seat: ET.Element):
        #Assume that if a seat has any of these definitions, is not available
        #[SD10 - RESTRICTED_SEAT_GENERAL -- SD11 - RESTRICTED -- SD19 - OCCUPIED],
        restrictedSeatDefs = ["SD10", "SD11","SD19"]
        availableSeatDef = "SD4"
        
        #Get seat definitions and check availability
        seatDefinitions =  self.__getSeatDefinitionsOfSeat(seat)
        hasAvailableSeatDef = any(availableSeatDef in seatDef for seatDef in seatDefinitions)
        isRestrictedSeat = False
        #Check if has restricted SeatDefs
        for restrictedDef in restrictedSeatDefs:
            if(any(restrictedDef in seatDef for seatDef in seatDefinitions)):
                isRestrictedSeat = True
                break
        return Availability(
            #Check if SD4(AVAILABLE) is in seatDefinitions
            value=hasAvailableSeatDef and not isRestrictedSeat,
            conditions=self.__seatDefinitionsToSeatConditions(seatDefinitions)
        )

    #Dict for seatConditons from seatDefinitions
    def __seatDefinitionsToSeatConditions(self,seatDefinitions):
        seatDefToSeatCondDict = {
            "SD1": SeatCondition.SEAT_SUITABLE_FOR_ADULT_WITH_AN_INFANT.name,
            "SD2": SeatCondition.SEAT_IN_A_QUIET_ZONE.name,
            "SD6": SeatCondition.SEAT_NOT_SUITABLE_FOR_CHILD.name,
            "SD7": SeatCondition.SEAT_NOT_ALLOWED_FOR_INFANT.name,
            "SD8": SeatCondition.RESTRICTED_RECLINE_SEAT.name,
            "SD9": SeatCondition.SEAT_TO_BE_LEFT_VACANT_OR_OFFERED_LAST.name,
            "SD12": SeatCondition.WING.name,
            "SD13": SeatCondition.SEAT_NOT_ALLOWED_FOR_MEDICAL.name,
            "SD14": SeatCondition.EXIT.name,
            "SD15": SeatCondition.LEG_SPACE_SEAT.name,
            "SD17": SeatCondition.SEAT_WITH_FACILITIES_FOR_HANDICAPPED.name,
            "SD18": SeatCondition.SEAT_WITH_FACILITIES_FOR_HANDICAPPED_INCAPACITATED_PASSENGER.name,
            "SD20": SeatCondition.SEAT_SUITABLE_FOR_UNACCOMPANIED_MINORS.name,
            "SD21": SeatCondition.REAR_FACING_SEAT.name,
            "SD22": SeatCondition.CREW_SEAT.name
        }
        seatConditions = []
        for seatDef in seatDefinitions:
            try:
                seatConditions.append(seatDefToSeatCondDict[seatDef]) 
            except:
                pass
        return seatConditions


            


