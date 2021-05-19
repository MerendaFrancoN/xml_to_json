class FlightOutputData:
    seatsData = []
    flightData = None

    def __init__(self, flightSeatsByRow, flightData):
        self.seatsData = flightSeatsByRow
        self.flightData = flightData

    def jsonRepr(self):
        return {
            "flightData":self.flightData,
            "seatsData":self.seatsData
        }