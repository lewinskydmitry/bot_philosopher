from abc import ABC, abstractmethod


class VendingMachineBuilder(ABC):

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def load_items(self):
        pass

    @abstractmethod
    def load_change(self):
        pass
