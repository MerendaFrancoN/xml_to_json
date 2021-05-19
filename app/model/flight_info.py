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

    def jsonRepr(self):
        return {
            "departureAirportCode":self.departureAirportCode,
            "arrivalAirportCode":self.arrivalAirportCode,
            "airEquipCode" : self.airEquipCode,
            "flightNumber" : self.flightNumber,
            "departureDateTime": self.departureDateTime 
        }