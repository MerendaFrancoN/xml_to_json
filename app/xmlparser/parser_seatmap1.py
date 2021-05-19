import xml.etree.ElementTree as ET
from app.xmlparser.parser_interface import SeatMapParserInterface
from app.model.flight_info import FlightInfo
from app.model.flight_seat import FlightSeat,SeatLocation, CabinType
from app.model.availability import Availability, SeatCondition
from app.model.price import Price

# Helpful link for a better understanding of fields meaning - 
# https://files.developer.sabre.com/doc/providerdoc/Merchandising/EnhancedSeatMap_v6_User_Guide.pdf
class SeatMap1Parser(SeatMapParserInterface):

    __namespaces = {
        'soapenc': "http://schemas.xmlsoap.org/soap/encoding/",
        'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
        'xsd': "http://www.w3.org/2001/XMLSchema",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'ns': "http://www.opentravel.org/OTA/2003/05/common/"
    }

    __fileTree = None
    __fileRoot = None
    __flightData = None

    # init method or constructor


    def __init__(self, file):
        self.__fileTree = ET.parse(file)
        self.__fileRoot = self.__fileTree.getroot()
        self.__flightData = self.__getFlightRawInfo()

    def __getBodyRoot(self):
        return self.__fileRoot.find("soapenv:Body", self.__namespaces)

    def __getFlightRawInfo(self):
        return self.__getBodyRoot().find("ns:OTA_AirSeatMapRS", self.__namespaces).find(
            "ns:SeatMapResponses", self.__namespaces).find("ns:SeatMapResponse", self.__namespaces).find(
                "ns:FlightSegmentInfo", self.__namespaces)

    def __getSeatMapRawDetails(self):
        return self.__getBodyRoot().find("ns:OTA_AirSeatMapRS", self.__namespaces).find(
            "ns:SeatMapResponses", self.__namespaces).find("ns:SeatMapResponse", self.__namespaces).find(
                "ns:SeatMapDetails", self.__namespaces)

    def __getCabinsData(self):
        return self.__getSeatMapRawDetails().findall("ns:CabinClass", self.__namespaces)

    def getFlightSeats(self) -> list:
        flightSeatList = []
        for cabinRowElement in self.__getCabinsData():
            cabinLayout = cabinRowElement.get("Layout")
            for seatRow in cabinRowElement:
                
                rowSeatsList = self.__parseRawRowSeat(seatRow, cabinLayout)
                flightSeatList.append(rowSeatsList)
        return flightSeatList

    def __parseRawRowSeat(self, row: ET.Element, cabinLayout: str):  # RowInfo
        seatsInRow = row.findall("ns:SeatInfo", self.__namespaces)
        seatsParsed = []
        for seatInfo in seatsInRow:
            flightSeat = FlightSeat(
                cabinClass=self.__parseCabinType(row),
                rowNumber=row.get("RowNumber"),
                availability=self.__parseAvailability(seatInfo),
                seatId=seatInfo.find(
                    "ns:Summary", self.__namespaces).get("SeatNumber"),
                location=self.__parseSeatLocation(seatInfo),
                price=Price(totalAmount=0.0, currency=""),
                cabinLayout=cabinLayout
            )
            # Update price of the seat
            flightSeat.price = self.__parseSeatPrice(
                seatInfo=seatInfo, isAvailable=flightSeat.availability.value)
            seatsParsed.append(flightSeat)

        return seatsParsed

    def __parseCabinType(self, rowInfoElement:ET.Element):
        cabinType = rowInfoElement.get("CabinType")
        if(cabinType == "Economy"):
            return CabinType.ECONOMY.name
        if(cabinType == "First"):
            return CabinType.FIRST.name          

    def __parseSeatLocation(self, seatInfo: ET.Element):
        
        features = seatInfo.findall(
                    "ns:Features", self.__namespaces)

        seatLocationStr = ""
        possibleSeatLocationsStrings = ["Aisle", "Window", "Center"]
        for feature in features:
            if(len(feature.keys()) == 0 and feature.text in possibleSeatLocationsStrings):
                seatLocationStr = feature.text
                break
        
        
        if(seatLocationStr == "Aisle"):
                return SeatLocation.AISLE.name
        if(seatLocationStr == "Window"):
                return SeatLocation.WINDOW.name
        if(seatLocationStr == "Center"):
                return SeatLocation.CENTER.name
        
        #If there is no info
        return SeatLocation.NO_INFO.name
        
    def __parseAvailability(self, seatInfo: ET.Element):

        seatConditions = []
        if(seatInfo.get("ExitRowInd") == "true"):
            seatConditions.append(SeatCondition.EXIT.name)

        #Parse all features and their "extension" tag
        extensions, featuresTexts = self.__parseFeatures(seatInfo)
        
        #Analyze extensions
        for extension in extensions:
            if(extension == "Limited Recline"):
                seatConditions.append(SeatCondition.RESTRICTED_RECLINE_SEAT.name)
            if(extension == "Chargeable"):
                seatConditions.append(SeatCondition.CHARGEABLE.name)
            if(extension == "Lavatory"):
                seatConditions.append(SeatCondition.LAVATORY.name)

        #Analyze texts
        for featureText in featuresTexts:
            if(featureText == "Overwing"):
                seatConditions.append(SeatCondition.WING.name)
            if(featureText == "BlockedSeat_Permanent"):
                seatConditions.append(SeatCondition.BLOCKED_SEAT_PERMANENT.name)
            
            

        return Availability(value=seatInfo.find(
            "ns:Summary", self.__namespaces).get("AvailableInd") == "true",
            conditions=seatConditions
        )

    def __parseFeatures(self, seatInfo):
        #Parse all features and their "extension" tag
        features = seatInfo.findall("ns:Features",self.__namespaces)
        extensions = []
        featuresTexts = []
        for feature in features:
            try:
                value = feature.get("extension")
                if value == None:
                    featuresTexts.append(feature.text)
                else:
                    extensions.append(value)
            except:
                pass
        return extensions, featuresTexts

    def __parseSeatPrice(self, seatInfo: ET.Element, isAvailable: bool):
        totalAmount = 0.0
        price = 0.0
        taxes = 0.0
        taxesCurrency = "" if not isAvailable else seatInfo.find(
            "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).find(
            "ns:Taxes", self.__namespaces).get("CurrencyCode").upper()
        priceCurrency = "" if not isAvailable else seatInfo.find(
            "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).get("CurrencyCode").upper()

        if(isAvailable):
            try:
                # TODO - Validate currency type
                price = float(seatInfo.find(
                    "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).get("Amount"))
                taxes = float(seatInfo.find(
                    "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).find("ns:Taxes", self.__namespaces).get("Amount"))
            except:
                price = 0.0
                taxes = 0.0

        totalAmount = price + taxes

        return Price(
            totalAmount=totalAmount,
            currency=priceCurrency
        )

    def getFlightInfo(self) -> FlightInfo:

        return FlightInfo(
            flightNumber=self.__flightData.get("FlightNumber"),
            departureDateTime=self.__flightData.get("DepartureDateTime"),
            airEquipCode=self.__flightData.find(
                "ns:Equipment", self.__namespaces).get("AirEquipType"),
            arrivalAirportCode=self.__flightData.find(
                "ns:ArrivalAirport", self.__namespaces).get("LocationCode"),
            departureAirportCode=self.__flightData.find(
                "ns:DepartureAirport", self.__namespaces).get("LocationCode"),
        )
