import xml.etree.ElementTree as ET
from app.model.flight_info import FlightInfo
from app.model.flight_seat import Availability, FlightSeat,SeatLocation
from app.model.price import Price

# --- Parsers ---- #


class Seat1MapParser:

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
            for seatRow in cabinRowElement:
                rowSeatsList = self.__parseRawRowSeat(seatRow)
                flightSeatList.append(rowSeatsList)
        return flightSeatList

    def __parseRawRowSeat(self, row: ET.Element):  # RowInfo
        seatsInRow = row.findall("ns:SeatInfo", self.__namespaces)
        seatsParsed = []
        for seatInfo in seatsInRow:
            flightSeat = FlightSeat(
                cabinClass=row.get("CabinType"),
                rowNumber=row.get("RowNumber"),
                availability=self.__parseAvailability(seatInfo),
                seatId=seatInfo.find(
                    "ns:Summary", self.__namespaces).get("SeatNumber"),
                location=self.__parseSeatLocation(seatInfo),
                price=Price(totalAmount=0.0, currency="")
            )
            # Update price of the seat
            flightSeat.price = self.__parseSeatPrice(
                seatInfo=seatInfo, isAvailable=flightSeat.availability.value)
            seatsParsed.append(flightSeat)

        return seatsParsed

    def __parseSeatLocation(self, seatInfo: ET.Element):
        
        features = seatInfo.findall(
                    "ns:Features", self.__namespaces)

        seatLocationStr = ""
        for feature in features:
            if(len(feature.keys()) == 0):
                seatLocationStr = feature.text
                break
        
        
        if(seatLocationStr == "Aisle"):
                return SeatLocation.AISLE.name
        if(seatLocationStr == "Window"):
                return SeatLocation.WINDOW.name
        if(seatLocationStr == "Center"):
                return SeatLocation.CENTER.name        
        
    def __parseAvailability(self, seatInfo: ET.Element):
        return Availability(value=seatInfo.find(
            "ns:Summary", self.__namespaces).get("AvailableInd") == "true",
            conditions=[]
        )

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