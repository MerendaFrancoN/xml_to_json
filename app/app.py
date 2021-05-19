import sys
from app.xmlparser.parser_seatmap1 import Seat1MapParser
from app.xmlparser.parser_seatmap2 import Seat2MapParser
from app.json_writer.json_writer import JSONFileWriter


def run():
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv[1]))
    # TODO -- Add control for args
    fileParser1 = Seat1MapParser(sys.argv[1])
    fileParser1.getFlightSeats()
    jsonWriter = JSONFileWriter()
    jsonWriter.flightSeatsByRowToJson(flightSeatsByRow=fileParser1.getFlightSeats(), flightData=fileParser1.getFlightInfo(),output_filename="data.json")
    
    
    #fileParser1 = Seat2MapParser(sys.argv[1])
    #jsonWriter = JSONFileWriter()
    #jsonWriter.flightSeatsToJson(flightSeats=fileParser1.getFlightSeats(),output_filename="data.json")

if __name__ == '__main__':
    run()