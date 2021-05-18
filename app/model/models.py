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
