class Price:
    totalAmount = 0.0
    currency = "USD"

    def __init__(self, totalAmount: float, currency: str):
        self.totalAmount = totalAmount
        self.currency = currency


