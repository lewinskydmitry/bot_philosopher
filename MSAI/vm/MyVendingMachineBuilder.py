from vm.VendingMachineBuilder import VendingMachineBuilder
from vm.PaymentOption import PaymentOption


class MyVendingMachineBuilder(VendingMachineBuilder):

    def build(self, myMachine):

        myMachine = self.load_items(myMachine)
        myMachine = self.load_change(myMachine)

        return myMachine

    def load_items(self, myMachine):

        # operator defined what vending items the machine will be capable to sell
        mars = ("Mars bar", 200)
        snickers = ("Snickers bar", 200)
        snickersXXL = ("Snickers XXL bar", 200)
        bounty = ("Bounty bar", 200)
        coke = ("Can of Coke", 150)
        dietCoke = ("Can of Diet Coke", 150)
        pythonBook = ("Python for Convex Problems", 506)  # yes, it is expensive!
        pythonBook2 = ("Software design patterns", 999)
        vending_items = set()
        vending_items.add(mars)
        vending_items.add(snickers)
        vending_items.add(snickersXXL)
        vending_items.add(bounty)
        vending_items.add(coke)
        vending_items.add(dietCoke)
        vending_items.add(pythonBook)
        vending_items.add(pythonBook2)
        myMachine.provision(vending_items)

        # operator loads vending items to the machine
        myMachine.add_inventory(0, mars, 30)
        myMachine.add_inventory(1, mars, 5)
        myMachine.add_inventory(2, mars, 15)
        myMachine.add_inventory(3, snickers, 10)
        myMachine.add_inventory(4, bounty, 10)
        myMachine.add_inventory(5, coke, 10)
        myMachine.add_inventory(6, dietCoke, 5)
        myMachine.add_inventory(7, pythonBook, 1)

        return myMachine

    def load_change(self, myMachine):

        # operator loads the machine with coins
        # machine need coins for change, because credit cards are not invented yet

        cashier = dict()
        cashier[PaymentOption(1, True)] = 500
        cashier[PaymentOption(5, True)] = 200
        cashier[PaymentOption(10, True)] = 100
        cashier[PaymentOption(25, True)] = 200
        cashier[PaymentOption(100, False)] = 2
        cashier[PaymentOption(500, False)] = 0
        cashier[PaymentOption(1000, False)] = 0
        cashier[PaymentOption(2000, False)] = 0
        myMachine.cashier = cashier
        return myMachine
