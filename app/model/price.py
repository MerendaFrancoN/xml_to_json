import json

class Price:
    totalAmount = 0.0
    currency = "USD"

    def __init__(self, totalAmount: float, currency: str):
        self.totalAmount = totalAmount
        self.currency = currency

    def jsonRepr(self):
        jsonDict = {
            "totalAmount": self.totalAmount,
            "currency": self.currency
        }
        return jsonDict

