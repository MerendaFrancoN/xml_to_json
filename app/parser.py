import xml.etree.ElementTree as ET

# ---Models --- #


class FlightInfo:
    departureAirportCode = ""
    arrivalAirportCode = ""
    airEquipCode = ""
    flightNumber = ""
    departureDateTime = ""

    def __init__(self, departureDateTime: str, flightNumber: str, airEquipCode: str, departureAirportCode: str, arrivalAirportCode: str):
        self.departureDateTime = departureDateTime
        self.arrivalAirportCode = arrivalAirportCode
        self.departureAirportCode = departureAirportCode
        self.airEquipCode = airEquipCode
        self.flightNumber = flightNumber


class Price:
    totalAmount = 0.0
    currency = "USD"

    def __init__(self, totalAmount: float, currency: str):
        self.totalAmount = totalAmount
        self.currency = currency


class FlightSeat:
    rowNumber = ""
    seatType = ""
    cabinClass = ""
    seatId = ""
    isAvailable = False
    price = Price(totalAmount=0.0, currency="")

    def __init__(self, seatType: str, cabinClass: str, seatId: str, isAvailable: bool, price: Price, rowNumber: str):
        self.seatType = seatType
        self.cabinClass = cabinClass
        self.seatId = seatId
        self.isAvailable = isAvailable
        self.price = price
        self.rowNumber = rowNumber


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

    def __parseRawRowSeat(self, row: ET.Element): #RowInfo
        seatsInRow = row.findall("ns:SeatInfo", self.__namespaces)
        seatsParsed = []
        for seatInfo in seatsInRow:
            flightSeat = FlightSeat(
                cabinClass=row.get("CabinType"),
                rowNumber=row.get("RowNumber"),
                isAvailable=seatInfo.find(
                    "ns:Summary", self.__namespaces).get("AvailableInd") == "true",
                seatId=seatInfo.find(
                    "ns:Summary", self.__namespaces).get("SeatNumber"),
                seatType=seatInfo.find(
                    "ns:Features", self.__namespaces).text,
                price= Price(totalAmount=0.0, currency="")
            )   
            #Update price of the seat
            flightSeat.price = self.__parseSeatPrice(seatInfo=seatInfo,isAvailable=flightSeat.isAvailable)

            seatsParsed.append(flightSeat)
            
        return seatsParsed

    def __parseSeatPrice(self,seatInfo: ET.Element, isAvailable : bool):
        return Price(
                totalAmount=0.0 if not isAvailable else seatInfo.find(
                    "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).get("Amount"),
                currency="" if not isAvailable else seatInfo.find(
                    "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).get("CurrencyCode").upper(),
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


class Seat2MapParser:

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
    __seatsMapDetailsRoot = None

    # init method or constructor

    def __init__(self, file):
        self.__fileTree = ET.parse(file)
        self.__fileRoot = self.__fileTree.getroot()
        self.__flightData = self.__getFlightRawInfo()
        self.__seatsMapDetailsRoot = self.__getSeatMapRawDetails()
        print(self.__seatsMapDetailsRoot)
        self.__getCabinsRows()

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

    def __parseRawRowSeat(self, row: ET.Element): #RowInfo
        seatsInRow = row.findall("ns:SeatInfo", self.__namespaces)
        seatsParsed = []
        for seatInfo in seatsInRow:
            flightSeat = FlightSeat(
                cabinClass=row.get("CabinType"),
                rowNumber=row.get("RowNumber"),
                isAvailable=seatInfo.find(
                    "ns:Summary", self.__namespaces).get("AvailableInd"),
                seatId=seatInfo.find(
                    "ns:Summary", self.__namespaces).get("SeatNumber"),
                seatType=seatInfo.find(
                    "ns:Features", self.__namespaces).text,
                price= Price(fee=0.0, currency="")
            )   
            flightSeat.price = Price(
                fee=0.0 if(flightSeat.isAvailable == "false") else seatInfo.find(
                    "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).get("Amount"),
                currency="" if (flightSeat.isAvailable == "false") else seatInfo.find(
                    "ns:Service", self.__namespaces).find("ns:Fee", self.__namespaces).get("CurrencyCode"),
            )
            seatsParsed.append(flightSeat)
            
        return seatsParsed

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
