import sys
from app.xmlparser.parser_seatmap1 import SeatMap1Parser
from app.xmlparser.parser_seatmap2 import SeatMap2Parser
from app.xmlparser.parser_selector import ParserSelector

from app.model.flight_output_data import FlightOutputData
from app.json_writer.json_writer import JSONFileWriter


def run():
    
    input_filename = str(sys.argv[1])
    parser = ParserSelector().getParser(input_filename)
    parseSeatMap(input_filename, parser)

def parseSeatMap(input_filename, parser):
    flightSeatsByRow = parser.getFlightSeats()
    flightData = parser.getFlightInfo()
    flightOutputData = FlightOutputData(flightSeatsByRow, flightData)
    outputFilename = input_filename+"_parsed.json"
    #Write JSON File
    JSONFileWriter().flightDataToJson(flightOutputData, output_filename=outputFilename)
    print("File {0} created successfully!".format(outputFilename.split(sep="/")[-1]))

if __name__ == '__main__':
    run()