import json

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
