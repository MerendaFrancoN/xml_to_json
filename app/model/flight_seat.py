from app.model.price import Price
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