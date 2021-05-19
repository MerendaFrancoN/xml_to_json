from app.model.flight_info import FlightInfo
import abc


#Abstract class to implement interface for parsers
class SeatMapParserInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getFlightSeats') and 
                callable(subclass.getFlightSeats) and 
                hasattr(subclass, 'getFlightInfo') and 
                callable(subclass.getFlightInfo) or 
                NotImplemented)

    @abc.abstractmethod
    def getFlightSeats(self) -> list:
        """Get Flight Seats By Row"""
        raise NotImplementedError

    @abc.abstractmethod
    def getFlightInfo(self) -> FlightInfo:
        """Get Flight Info"""
        raise NotImplementedError