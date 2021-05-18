import sys
from app.xmlparser.parser import Seat1MapParser


def run():
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv[1]))
    # TODO -- Add control for args
    fileParser1 = Seat1MapParser(sys.argv[1])
    flightInfo1 = fileParser1.getFlightInfo()
    flightSeats1 = fileParser1.getFlightSeats()
    print("FInished")


if __name__ == '__main__':
    run()