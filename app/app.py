import sys
from app.xmlparser.parser_seatmap1 import Seat1MapParser
from app.xmlparser.parser_seatmap2 import Seat2MapParser


def run():
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv[1]))
    # TODO -- Add control for args
    fileParser1 = Seat2MapParser(sys.argv[1])


if __name__ == '__main__':
    run()