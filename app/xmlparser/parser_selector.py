from app.xmlparser.parser_seatmap1 import SeatMap1Parser
from app.xmlparser.parser_seatmap2 import SeatMap2Parser

class ParserSelector:

    def getParser(self, input_filename):
        parser = None
        try:
            parser = SeatMap1Parser(input_filename)
            return parser
        except:
            pass

        try:
            parser = SeatMap2Parser(input_filename)
            return parser
        except:
            print("Failed while attempting to parse with Both Parsers - Check File Format")

        return None

        



