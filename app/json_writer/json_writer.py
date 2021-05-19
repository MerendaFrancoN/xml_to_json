import json
from app.model.flight_output_data import FlightOutputData

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'jsonRepr'):
            return obj.jsonRepr()
        else:
            return json.JSONEncoder.default(self, obj)

class JSONFileWriter:

    def flightSeatsToJson(self, flightSeats : list,output_filename: str):
        jsonString = ""
        for flightSeat in flightSeats:
            jsonString+=json.dumps(flightSeat.jsonRepr(), cls=ComplexEncoder, indent=4)
        
        jsonFile = open(output_filename, "w")
        jsonFile.write(jsonString)
        jsonFile.close()
    
    def flightSeatsByRowToJson(self, flightSeatsByRow : list, flightData,output_filename: str):
        
        jsonFile = open(output_filename, "w")
        jsonString = json.dumps(FlightOutputData(flightSeatsByRow, flightData).jsonRepr(), cls=ComplexEncoder, indent=2)
        jsonFile.write(jsonString)
        jsonFile.close()