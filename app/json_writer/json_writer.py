import json
from app.model.flight_output_data import FlightOutputData

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'jsonRepr'):
            return obj.jsonRepr()
        else:
            return json.JSONEncoder.default(self, obj)

class JSONFileWriter:
    
    def flightDataToJson(self, flightData: FlightOutputData, output_filename: str):
        jsonFile = open(output_filename, "w")
        jsonString = json.dumps(flightData.jsonRepr(), cls=ComplexEncoder, indent=2)
        jsonFile.write(jsonString)
        jsonFile.close()
        