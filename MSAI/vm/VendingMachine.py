from abc import ABC, abstractmethod, abstractproperty


class VendingMachine(ABC):
    @abstractmethod
    def provision(self, vending_items):
        pass

    @abstractmethod
    def add_inventory(self, shelf, vending_item, quantity):
        pass

    @abstractmethod
    def substract_money_from_cashier(self, paymentMethod, quantity):
        pass

    @abstractmethod
    def purchase_item(self, shelfNumber, payments):
        pass

    # use case #2.A - Vendor gets a report on which items are left in the machine
    @property
    @abstractmethod
    def inventory(self):
        pass

    @property
    @abstractmethod
    def cashier(self):
        pass

    # use case #3 - Vendor fills the machine with coins for change
    @cashier.setter
    @abstractmethod
    def cashier(self, value):
        pass
