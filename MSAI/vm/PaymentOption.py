class PaymentOption:
    def __init__(self, value, returnable):
        self.__value = value
        self.__returnable = returnable

    @property
    def value(self):
        return self.__value

    @property
    def returnable(self):
        return self.__returnable


