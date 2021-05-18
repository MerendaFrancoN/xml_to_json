import xml.etree.ElementTree as ET
from app.model.flight_info import FlightInfo
from app.model.flight_seat import FlightSeat
from app.model.price import Price


class Seat2MapParser:

    __namespaces = {
        'ns': "http://www.iata.org/IATA/EDIST/2017.2",
        'ns2': "http://www.iata.org/IATA/EDIST/2017.2/CR129"
    }

    __fileTree = None
    __fileRoot = None
    __offerItems = {}
    __seatDefinitions = {}

    # init method or constructor

    def __init__(self, file):
        self.__fileTree = ET.parse(file)
        self.__fileRoot = self.__fileTree.getroot()
        self.__offerItems = self.__parseAlaCarteOffer()
        self.__seatDefinitions = self.__parseSeatDefinitions()


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
    
    
    def __parseSeatDefinitions(self):
        seatDefs = {}
        seatDefinitionList = self.__fileRoot.find("ns:DataLists",self.__namespaces).find("ns:SeatDefinitionList",self.__namespaces)
        
        for seatDefinition in seatDefinitionList:
            seatDefKey = seatDefinition.get("SeatDefinitionID")
            seatDefs[seatDefKey] = seatDefinition.find("ns:Description",self.__namespaces).find("ns:Text",self.__namespaces).text
        
        return seatDefs

    def __parseSeatsData(self):
        seatMapList = self.__fileRoot.find("ns:SeatMap",self.__namespaces)
        for seatMap in seatMapList:
            seatRows = seatMap.find("ns:Cabin",self.__namespaces).findall("ns:Row",self.__namespaces)
            for row in seatRows:
                seats = row.findall("ns:Seat",self.__namespaces)
                rowNumber = row.find("ns:Number",self.__namespaces).text
                for seat in seats:
                    colNumber = seat.find("ns:Column",self.__namespaces).text
                    seatId = str(rowNumber)+str(colNumber)
                    priceRef = seat.find("ns:OfferItemRefs",self.__namespaces)
                    
    def __getPriceFromOfferRef(self, priceRef):
        if(priceRef != None):
            return self.__offerItems.get(priceRef)
        
        return Price(currency="", totalAmount=0.0)


            


