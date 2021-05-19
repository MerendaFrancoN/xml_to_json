import sys
from app.xmlparser.parser_seatmap1 import Seat1MapParser
from app.xmlparser.parser_seatmap2 import Seat2MapParser
from app.model.flight_output_data import FlightOutputData
from app.json_writer.json_writer import JSONFileWriter


def run():
    
    input_filename = str(sys.argv[1])

    #Add Selector

    parseSeatMap2(input_filename)

def parseSeatMap1(input_filename):
    seatmap1_parser = Seat1MapParser(input_filename)
    flightSeatsByRow = seatmap1_parser.getFlightSeats()
    flightData = seatmap1_parser.getFlightInfo()
    JSONFileWriter().flightDataToJson(FlightOutputData(flightSeatsByRow, flightData),output_filename=input_filename+"_parsed.json")

def parseSeatMap2(input_filename):
    seatmap2 = Seat2MapParser(input_filename)
    flightSeatsByRow = seatmap2.getFlightSeats()
    #flightData = seatmap2.getFlightInfo()
    JSONFileWriter().flightDataToJson(FlightOutputData(flightSeatsByRow, {}),output_filename=input_filename+"_parsed.json")

if __name__ == '__main__':
    run()